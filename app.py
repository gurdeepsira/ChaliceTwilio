from chalice import Chalice, Response
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

tw_client = Client(ACCOUNT_SID, AUTH_TOKEN)


app = Chalice(app_name='ChaliceTwilio')


app = Chalice(app_name='sms-shooter')

# Create a Twilio client using account_sid and auth token
tw_client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route('/service/sms/send', methods=['POST'])
def send_sms():
    request_body = app.current_request.json_body
    if request_body:
        try:
            msg = tw_client.messages.create(
                from_=FROM_NUMBER,
                body=request_body['msg'],
                to=TO_NUMBER)

            if msg.sid:
                return Response(status_code=201,
                                headers={'Content-Type': 'application/json'},
                                body={'status': 'success',
                                      'data': msg.sid,
                                      'message': 'SMS successfully sent'})
            else:
                return Response(status_code=200,
                                headers={'Content-Type': 'application/json'},
                                body={'status': 'failure',
                                      'message': 'Please try again!!!'})
        except TwilioRestException as exc:
            return Response(status_code=400,
                            headers={'Content-Type': 'application/json'},
                            body={'status': 'failure',
                                  'message': exc.msg})
