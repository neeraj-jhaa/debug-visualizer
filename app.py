from flask import Flask, render_template, request, send_from_directory
import sys
import io
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-code", methods=["POST"])
def run_code():
    user_code = request.form["user_code"]
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()

    try:
        exec(user_code)
        result = redirected_output.getvalue()

        # Output se numbers collect karo
        numbers = []
        for line in result.splitlines():
            try:
                numbers.append(float(line))
            except:
                pass

        if numbers:
            fig, ax = plt.subplots()
            x_data, y_data = [], []
            line, = ax.plot([], [], 'r-', marker='o')
            ax.set_xlim(0, len(numbers))
            ax.set_ylim(min(numbers)-1, max(numbers)+1)
            ax.set_title("Live Code Output Graph 📊")
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")

            def update(frame):
                x_data.append(frame)
                y_data.append(numbers[frame])
                line.set_data(x_data, y_data)
                return line,

            ani = FuncAnimation(fig, update, frames=range(len(numbers)), blit=True, repeat=False)

            if not os.path.exists("static"):
                os.mkdir("static")

            ani.save("static/output_graph.gif", writer='pillow')
            plt.close()

            graph_html = "<h3>Motion Graph:</h3><img src='/static/output_graph.gif'>"
        else:
            graph_html = ""

    except Exception as e:
        result = str(e)
        graph_html = ""
    finally:
        sys.stdout = old_stdout

    return f"<h2>Result:</h2><pre>{result}</pre>{graph_html}<br><a href='/'>Wapas Jao</a>"

if __name__ == "__main__":
    app.run(debug=True)
