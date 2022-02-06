from flask import Flask, redirect, render_template, request, url_for
import sqlite3
import datetime
from manage import verified_delete, idgenerated, get_data, repeate_tasks, insert_repeated_task
import threading

app = Flask(__name__)

get_data()

task_data_for_table0, task_data_for_relevance0, list_true0,  = get_data()


@app.route('/table.html', methods=['GET', 'POST'])
def table():
    return render_template('table.html',  task_table=task_data_for_table0,task_relevance=task_data_for_relevance0, task_true=list_true0)


@app.route('/insert.html', methods=['GET', 'POST'])
def insert():
    conn = sqlite3.connect('todo')
    c = conn.cursor()

    verified_delete(completed=request.form.getlist('options'))
    insert_repeated_task()

    if request.method == "POST":
        if request.form['action'] == 'Submit':

            date_time_sql = datetime.datetime.now()
            name = request.form['lname']
            request_date = request.form['meeting-time']
            request_date2 = str(request_date).replace('T', ' ')
            mesaj = 'no deadline'
            important = request.form['selectare_importanta']
            dead_line_repeat = request.form['dead_line_repeat']
            newid=idgenerated()

            if dead_line_repeat == "1" and request_date == "":

                query1 = f'INSERT INTO tasks (text, task_creation_time, dead_line, completed, relevance, id_generated)  VALUES("{name}", "{date_time_sql}","{mesaj}", "False", "{important}", "{newid}")'
                c.execute(query1)
                conn.commit()
            elif dead_line_repeat == "1":
                query1 = f'INSERT INTO tasks (text, task_creation_time, dead_line, completed, relevance, id_generated)  VALUES("{name}", "{date_time_sql}","{request_date2}", "False", "{important}", "{newid}")'
                c.execute(query1)
                conn.commit()
            elif dead_line_repeat == "2":
                add = datetime.timedelta(days=1)
                repeate_tasks(request_date2, add, name, date_time_sql, important, newid)
            elif dead_line_repeat == "3":
                add = datetime.timedelta(days=7)
                repeate_tasks(request_date2[:+10], add, name, date_time_sql, important, newid)
            elif dead_line_repeat == "4":
                add = datetime.timedelta(weeks=4)
                repeate_tasks(request_date2[:+10], add, name, date_time_sql, important, newid)
            elif dead_line_repeat == "5":
                add = datetime.timedelta(days=365)
                repeate_tasks(request_date2[:+10], add, name, date_time_sql, important, newid)



            task_data_for_table, task_data_for_relevance, list_true = get_data()
            return render_template('insert.html', task_table=task_data_for_table,task_relevance=task_data_for_relevance, task_true=list_true)

        if request.form['action'] == "Delete":
            data_generated = datetime.datetime.now()
            completed = request.form.getlist('options')
            c.execute("SELECT task_creation_time FROM tasks ")

            update_completed_time = []
            for each in c.fetchall():
                update_completed_time.append(each)

            for each in completed:
                each_element_update = str(update_completed_time[int(each)]) .replace('(', '') .replace(')', '') .replace(',', '')
                query5 = f'UPDATE tasks SET completed_time = "{data_generated}" WHERE task_creation_time ={each_element_update}'
                c.execute(query5)
                conn.commit()


            c.execute("SELECT completed_time FROM tasks")
            delete_completed_time = []

            for every in c.fetchall():
                delete_completed_time.append(every)
            for every in completed:

                every_element_delete =str(delete_completed_time[int(every)]) .replace('(', '') .replace(')', '') .replace(',', '').replace('\"', '').replace('\'', '')

                every_element_delete = datetime.datetime.strptime(every_element_delete, '%Y-%m-%d %H:%M:%S.%f')
                add_1 = datetime.timedelta(minutes=-1)
                delete_after_time = every_element_delete + add_1

                query3 = f'DELETE FROM tasks WHERE completed_time <= "{every_element_delete}" '
                c.execute(query3)
                conn.commit()
            try:
                c.execute("SELECT id_generated FROM repeat_task")
                test_list =[]
                for a in c.fetchall():
                    test_list.append(a[0])
                for a in completed:
                    delete_repeat_tasks = str(test_list[int(a)])

                    query4 = f'DELETE FROM repeat_task WHERE id_generated = "{delete_repeat_tasks}"'
                    c.execute(query4)
                    conn.commit()
            except Exception as b:
                print(b)

            task_data_for_table, task_data_for_relevance, list_true = get_data()
            return render_template('insert.html', task_table=task_data_for_table,task_relevance=task_data_for_relevance, task_true=list_true)


    task_data_for_table0, task_data_for_relevance0, list_true0 = get_data()
    return render_template('insert.html', task_table=task_data_for_table0, task_relevance=task_data_for_relevance0,task_true=list_true0)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='POST':
        if request.form['action'] == "Add task here":
            return redirect(url_for(insert()))
        elif request.form['action'] == "View tasks":
            return render_template('table.html')
    return render_template('index.html')

if __name__ == '__main__':
    x =threading.Thread(target=insert_repeated_task)
    x.start()
    app.run(debug=True)