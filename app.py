from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from views import login_view
from controllers import show_contact_list, show_contacts_edit, do_register, do_login, do_delete_contact, do_add_contact, do_edit_contact

current_user = None

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('GET')
        global current_user

        parsed_path = urlparse(self.path)

        if current_user is None:
            print('No user - using login_view')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = login_view()
            self.wfile.write(response.encode())

        elif parsed_path.path == '/':
            # Handle contact list request
            req_params = parse_qs(parsed_path.query)
            sorting = req_params.get('sorting', ['name'])[0]
            print(f'Main page for user={current_user.username}, sorting={sorting}')
            response = show_contact_list(current_user, sorting)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode())

        elif parsed_path.path == '/logout/':
            current_user=None
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif parsed_path.path.startswith('/edit_contact/'):
            # Handle edit contact request
            contact_id=int(parsed_path.path.split('/')[2])
            response = show_contacts_edit(contact_id)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode())

        elif parsed_path.path.startswith('/delete_contact/'):
            # Handle delete contact request
            contact_id=int(parsed_path.path.split('/')[2])
            print(f'delete contact id={contact_id}')
            do_delete_contact(contact_id)
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            pass


        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("404 Not Found".encode())


    def do_POST(self):
        print('POST')

        global current_user

        parsed_path = urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        if content_length > 0:
            req_data = self.rfile.read(content_length).decode('utf-8')
            req_params = parse_qs(req_data)
        else:
            req_params={}

        if parsed_path.path == '/login':
            # Handle login request
            print('LOGIN')
            username = req_params.get('username', [''])[0]
            password = req_params.get('password', [''])[0]
            user=do_login(username=username, password=password)
            if user:
                current_user=user
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response = login_view(text_response="Invalid username or password!")
                self.wfile.write(response.encode())

        elif parsed_path.path == '/register':
            # Handle registration request
            print('REGISTER')
            username = req_params.get('username', [''])[0]
            password = req_params.get('password', [''])[0]
            new_user=do_register(username,password)
            if new_user:
                current_user=new_user
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response = login_view(text_response="Error registering. Username already in the database!")
                self.wfile.write(response.encode())

        elif parsed_path.path == '/add_contact':
            # Handle add contact request
            name = req_params.get('name', [''])[0]
            email = req_params.get('email', [''])[0]
            phone = req_params.get('phone', [''])[0]
            print(f'add contact user={current_user.username}, name={name},email={email},phone={phone}')
            do_add_contact(current_user,name,email,phone)
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        elif parsed_path.path.startswith('/edit_contact/'):
            # Handle edit contact submission
            contact_id = int(parsed_path.path.split('/')[2])
            name = req_params.get('name', [''])[0]
            email = req_params.get('email', [''])[0]
            phone = req_params.get('phone', [''])[0]
            print(f'edit contact id={contact_id}, name={name},email={email},phone={phone}')
            do_edit_contact(contact_id,name,email,phone)
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("404 Not Found".encode())


def start_server():
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server started on http://localhost:8080")
    httpd.serve_forever()


if __name__ == '__main__':
    start_server()


