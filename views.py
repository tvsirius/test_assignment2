def login_view(text_response=""):
    html = f"""
    <html>
    <head>
        <title>Login</title>
    </head>
    <body>
    {"<br><br><b>"+text_response+"</b><br>" if text_response else ""}       
    <h1>Login</h1>
        <form method="post" action="/login">
            <label>Username: <input type="text" name="username" required></label><br>
            <label>Password: <input type="password" name="password" required></label><br>
            <input type="submit" value="Sign In">
        </form>
        <br>
        <h2>Register New User</h2>
        <form method="post" action="/register">
            <label>Username: <input type="text" name="username" required></label><br>
            <label>Password: <input type="password" name="password" required></label><br>
            <input type="submit" value="Register">
        </form>
    </body>
    </html>
    """
    return html



def contacts_view(contact_list, username):
    html = f"""
    <html>
    <head>
        <title>Contact List</title>
    </head>
    <body>
        <h1>Contact List</h1>
                    <h2>Hello, {username}</h2>
                    <a href="/logout/">Log-out</a>
                    <br><br><br>
        <table>
            <tr>
                <th><a href="/?sorting=name">Name</a></th>
                <th><a href="/?sorting=email">Email</a></th>
                <th>Phone</th>
                <th>Actions</th>
            </tr>
    """

    for contact in contact_list:
        html += """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>
                    <a href="/edit_contact/{}">Edit</a>
                    <a href="/delete_contact/{}">Delete</a>
                </td>
            </tr>
        """.format(contact.name, contact.email, contact.phone, contact.id, contact.id)

    html += """
        </table>
        <h2>Add New Contact</h2>
        <form method="post" action="/add_contact">
            <label>Name: <input type="text" name="name" required></label><br>
            <label>Email: <input type="text" name="email"></label><br>
            <label>Phone: <input type="text" name="phone"></label><br>
            <input type="submit" value="Add Contact">
        </form>
    </body>
    </html>
    """

    return html



def contacts_edit_view(contact):
    html = """
    <html>
    <head>
        <title>Edit Contact</title>
    </head>
    <body>
        <h1>Edit Contact</h1>
        <form method="post" action="/edit_contact/{}">
            <label>Name: <input type="text" name="name" value="{}"></label><br>
            <label>Email: <input type="text" name="email" value="{}"></label><br>
            <label>Phone: <input type="text" name="phone" value="{}"></label><br>
            <input type="submit" value="Save Changes">
        </form>
    </body>
    </html>
    """.format(contact.id, contact.name, contact.email, contact.phone)

    return html

#
