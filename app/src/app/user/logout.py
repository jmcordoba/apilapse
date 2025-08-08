from flask import request, jsonify, make_response

class UserLogout:
    """
    Class responsible for logging out a user and removing all cookies.
    """
    def logout(self):
        """
        Remove all cookies to log out the user.
        """
        try:
            # Create a response object
            resp = make_response(jsonify({"message": "Logout successful"}))

            # Remove cookies by setting their expiration dates to a past date
            cookies_to_remove = ['Access-Token', 'Refresh-Token']
            for cookie in cookies_to_remove:
                resp.set_cookie(cookie, '', expires=0, path='/', domain=request.host)

            return resp

        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"message": "An error occurred while logging out the user"}), 500
