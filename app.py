from flask import Flask, request, Response, redirect
import vc
import os
import utils
import collections

app = Flask(__name__)

@app.route("/", methods=['post'])
def hello():
    '''
    Example message:
    /vc a16z p
    /vc instagram i
    '''
    message = request.values.get('text')

    arr = message.split(" ")

    result = {}
    response = ""
    # look up VC's portfolio
    if arr[1] == "p":
        result = vc.getPortfolio(arr[0].lower())
        result = collections.OrderedDict(sorted(result.items()))
        response = ":innocent: This is " + vc.getVCName(arr[0].lower()) + "'s portfolio: \n\n"
        i = 1
        for k, v in result.items():
            response += "<" + v.strip() + "|" + str(i) + ". " + utils.extract_name_from_string(k.strip()) + ">\n"
            i += 1
    # look up a company's backed investors
    elif arr[1] == "i":
        result = vc.getInvestors(arr[0].lower())
        result = collections.OrderedDict(sorted(result.items()))
        response = ":innocent: These are " + arr[0] + "'s investors: \n"
        i = 1
        for k, v in result.items():
            response += "<" + v.strip() + "|" + str(i) + ". " + str(k) + ">\n"
            i += 1
    else:
        response = ":innocent: This command is not supported, please re-type :innocent:\n"
    return Response(response, content_type='text/plain;charset=utf-8')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
