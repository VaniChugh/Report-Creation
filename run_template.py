from __future__ import division
from datetime import datetime
from jinja2 import Environment

testsuitename = "FIX_Test_Suite"

testcaseInfo = {'123': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 123"},
                        "Expected Outputs": {"CAMM Message": "Message Output1"},
                        "Actual CAMM Response": {"EcnReqID": "123", "Quantity": "2"},
                        "Actual FIX Response": {"ReqID": "123123", "orderID": "2"},
                        "Result": {"OverallResult": "PASS",
                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '234': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 234"},
                                        "Expected Outputs": {"CAMM Message": "Message Output1"},
                                        "Actual CAMM Response": {"EcnReqID": "234", "Quantity": "2"},
                                        "Actual FIX Response": {"ReqID": "234234", "orderID": "2"},
                                        "Result": {"OverallResult": "FAIL",
                                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '345': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 345"},
                                        "Expected Outputs": {"CAMM Message": "Message Output1"},
                                        "Actual CAMM Response": {"EcnReqID" : "345", "Quantity": "2"},
                                        "Actual FIX Response": {"ReqID" : "345345", "orderID": "2"},
                                        "Result": {"OverallResult": "PASS",
                                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '456': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 456"},
                        "Expected Outputs": {"CAMM Message": "Message Output1"},
                        "Actual CAMM Response": {"EcnReqID" : "456", "Quantity": "2"},
                        "Actual FIX Response": {"ReqID": "456456", "orderID": "2"},
                        "Result": {"OverallResult": "PASS",
                                  "Actual CAMM Message": "Hello this the CAMM Message",
                                  "Actual FIX Message": "Hello this is the FIX Message."}}
                }

# using the route decorator to tell the Flask what URL should trigger our function
def template_test():
    test_case_result = {}
    for testcase in testcaseInfo:
        test_case_result[testcase] = testcaseInfo[testcase]["Result"]["OverallResult"]

    input_length = 0
    camm_message_length = 0
    fix_message_length = 0
    for elem in testcaseInfo:
        input_length=len(testcaseInfo[elem]["Inputs"])
        camm_message_length=len(testcaseInfo[elem]["Actual CAMM Response"])
        fix_message_length=len(testcaseInfo[elem]["Actual FIX Response"])

    input_fields = []
    camm_message_fields = []
    fix_message_fields = []
    for elem in testcaseInfo:
        for elem1 in testcaseInfo[elem]:
            print(elem1)
            if elem1 == "Inputs":
               print("Here")
               for input_value in testcaseInfo[elem][elem1]:
                   if input_value not in input_fields:
                        input_fields.append(input_value)
            elif elem1 == "Actual CAMM Response":
               print("Here1")
               for input_value in testcaseInfo[elem][elem1]:
                   if input_value not in camm_message_fields:
                        camm_message_fields.append(input_value)
            elif elem1 ==  "Actual FIX Response":
               print("Here2")
               for input_value in testcaseInfo[elem][elem1]:
                   if input_value not in fix_message_fields:
                        fix_message_fields.append(input_value)


    print(input_fields)
    print(fix_message_fields)
    print(camm_message_fields)

    testcasedetails = test_case_result
    count = 0
    for dv in testcasedetails.values():
        if dv == "PASS":
            count = count + 1

    total = len(testcasedetails)
    teststatus = [testsuitename, total, count, total - count, str(round((count / total) * 100, 1))]
    try:
        with open("./templates/template.html", 'r') as temp1:
            htmlval = temp1.read()
            jinja_env = Environment().from_string(htmlval).render(title="Test Execution Report: {}".format(testsuitename),
                                                                  testsuite=testsuitename,
                                                                  statusdet=teststatus,
                                                                  td=testcaseInfo,
                                                                  input_length=input_length,
                                                                  camm_message_length=camm_message_length,
                                                                  fix_message_length=fix_message_length,
                                                                  input_fields = input_fields,
                                                                  camm_message_fields= camm_message_fields,
                                                                  fix_message_fields=fix_message_fields)

            timestamp = datetime.timestamp(datetime.now())
            report_filename = "./reports/report_{}_{}.html".format(testsuitename, timestamp)
            with open(report_filename, 'w') as report:
                report.write(jinja_env)
        return "Success"
    except FileNotFoundError:
        print("File not found")
        return "Failed"

if __name__ == '__main__':
    template_test()