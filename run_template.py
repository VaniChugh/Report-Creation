from __future__ import division
from flask import Flask,render_template
from jinja2 import Environment
test_case_result = {'123': "Pass",
                    '234': "Fail",
                    '345': "Skip",
                    '456': "Pass"}
app = Flask(__name__)

@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter


# using the route decorator to tell the Flask what URL should trigger our function
@app.route("/")
def template_test():
    testcasedetails = test_case_result
    count = 0
    for dv in testcasedetails.values():
        if "Pass" in dv:
            count = count + 1
    total = len(testcasedetails)
    algebrastatus = ["Algebra", total, count, total - count, str(round((count / total) * 100, 1))]
    print(algebrastatus)
    try:
        with open("./templates/template.html", 'r') as temp1:
            htmlval = temp1.read()
            jinja_env = Environment().from_string(htmlval).render(title = "Test Case Summary",
                                                                  testsuite="FIX test Suite",
                                                                  statusdet= algebrastatus,
                                                                  td=test_case_result,)
            print(jinja_env)
            with open("./reports/report.html", 'w') as report:
                report.write(jinja_env)
    except FileNotFoundError:
        print("File not found")
    # return render_template('template.html',
    #                        my_string="Wheeeee!",
    #                        test_case_result=test_case_result,
    #                        my_list=[0, 1, 2, 3, 4, 5],
    #                        testsuite="FIX test Suite",
    #                        current_time=datetime.datetime.now())

if __name__ == '__main__':
    app.run(debug=True)