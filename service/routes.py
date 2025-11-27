"""
Account Service

This microservice handles the lifecycle of Accounts
"""
from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Account

# Import Flask application
from service import app


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


############################################################
# Index page
############################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


############################################################
# CREATE A NEW ACCOUNT
############################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    try:
        account.deserialize(request.get_json())
    except Exception as e:
        app.logger.error("Error deserializing account: %s", str(e))
        abort(status.HTTP_400_BAD_REQUEST, str(e))

    account.create()
    message = account.serialize()
    location_url = url_for("get_accounts", account_id=account.id, _external=True)

    app.logger.info("Account with ID [%s] created.", account.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


############################################################
# READ AN ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
    Reads an Account
    This endpoint will read an Account based on the account_id that is requested
    """
    app.logger.info("Request to read an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    app.logger.info("Returning account: %s", account.name)
    return jsonify(account.serialize()), status.HTTP_200_OK


############################################################
# LIST ALL ACCOUNTS
############################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """
    List all Accounts
    This endpoint will list all Accounts
    """
    app.logger.info("Request to list Accounts")

    accounts = Account.all()

    account_list = [account.serialize() for account in accounts]
    app.logger.info("Returning %d accounts", len(account_list))
    return jsonify(account_list), status.HTTP_200_OK


############################################################
# UPDATE AN EXISTING ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    """
    Update an Account
    This endpoint will update an Account based on the posted data
    """
    app.logger.info("Request to update an Account with id: %s", account_id)

    account = Account.find(account_id)
    if not account:
        abort(status.HTTP_404_NOT_FOUND, f"Account with id [{account_id}] could not be found.")

    account.deserialize(request.get_json())
    account.update()

    app.logger.info("Account with ID [%s] updated.", account.id)
    return jsonify(account.serialize()), status.HTTP_200_OK


############################################################
# DELETE AN ACCOUNT
############################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    """
    Delete an Account
    This endpoint will delete an Account based on the account_id that is requested
    """
    app.logger.info("Request to delete an Account with id: %s", account_id)

    account = Account.find(account_id)
    if account:
        account.delete()
        app.logger.info("Account with ID [%s] deleted.", account_id)

    return "", status.HTTP_204_NO_CONTENT


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
