import psutil
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns
import datetime as dt
from time import sleep
# import PyQt5
import matplotlib as mpl
mpl.use("Qt5Agg")


class Resources:

    def __init__(self):
        self.res_act = []
        self.cache = []
        self.figures = {}


class HwResources(Resources):

    def __int__(self):
        super.__init__()

    def update(self):

        def check_lst_len(n: int, lst: list):
            if len(lst) > n:
                print(f"after len: {len(lst)}")
                lst.pop(0)
                print(f"after len: {len(lst)}")

        self.res_act = [psutil.cpu_percent(interval=1),
                        psutil.virtual_memory()[2],
                        psutil.disk_usage("/"),
                        psutil.disk_io_counters(),
                        psutil.net_io_counters(),
                        ]

        now = dt.datetime.now()
        self.cache.append({now.strftime("%H:%M:%S"): self.res_act})
        check_lst_len(60, self.cache)
        print(self.res_act)
        self.create_donut_plot(n=self.res_act[0], key="cpu_act", title="CPU Load", width=250)
        self.create_donut_plot(n=self.res_act[1], key="ram_act", title="RAM Load", width=250)
        self.create_donut_plot(n=self.res_act[2][3], key="hdd_usage", title="HDD Usage", width=250)

        x_all = []
        y_cpu = []
        for rec in self.cache:
            for k, v in rec.items():
                x_all.append(k)
                y_cpu.append(v[0])

        self.create_line_plot(x=x_all,
                              y=y_cpu,
                              key="cpu_history",
                              title="CPU History",
                              width=600)

        y_ram = []
        for rec in self.cache:
            for val in rec.values():
                y_ram.append(val[1])

        self.create_line_plot(x=x_all,
                              y=y_ram,
                              key="ram_history",
                              title="RAM History",
                              width=600
                              )

        y_hdd_all = []
        y_hdd_rc = []
        y_hdd_wc = []
        y_hdd_rt = []
        y_hdd_wt = []

        for rec in self.cache:
            for val in rec.values():
                y_hdd_rc.append(val[3][0])
                y_hdd_wc.append(val[3][1])
                y_hdd_rt.append(val[3][4])
                y_hdd_wt.append(val[3][5])
            y_hdd_all = [y_hdd_rc, y_hdd_wc, y_hdd_rt, y_hdd_wt]

        self.create_hdd_line_plot(x=x_all,
                                  y=y_hdd_all,
                                  key="hdd_history",
                                  title="HDD IOPS Performance",
                                  width=600,
                                  )

        y_net_all = []
        y_net_out = []
        y_net_in = []

        for rec in self.cache:
            for val in rec.values():
                y_net_out.append(val[4][0])
                y_net_in.append(val[4][1])
                y_net_all = [y_net_in, y_net_out]

        self.create_net_line_plot(x=x_all,
                                  y=y_net_all,
                                  key="net_history",
                                  title="Network Performance",
                                  width=600)

    def run(self):
        for i in range(3):
            self.update()
            sleep(5)

    def create_donut_plot(self, n: float, key: str, title: str):
        values = [n, 100-n]
        colors = [None, "lightgrey"]
        if n < 40:
            colors[0] = "g"
            edgecolor = "g"
        elif n < 80:
            colors[0] = "y"
            edgecolor = "y"
        else:
            colors[0] = "r"
            edgecolor = "r"

        fig = plt.figure(figsize=(3, 3))

        plt.pie(values,
                startangle=90,
                wedgeprops={"width": 0.25, "edgecolor": edgecolor, "lw": 1},
                colors=colors)
        plt.text(0, 0, s=f"{values[0]}%", ha="center", va="center", fontsize=24)
        plt.title(title, fontsize=18)
        # fig.set_facecolor("black")

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        img = f"data:image/png;base64,{data}"
        self.figures[key] = img
        plt.close()

    def create_line_plot(self, x: list, y: list, key: str, title: str):
        sns.set_theme(style="darkgrid")
        fig = plt.figure(figsize=(26, 3))
        plt.title(title, fontsize=18)

        sns.lineplot(x=x, y=y)

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        img = f"data:image/png;base64,{data}"
        self.figures[key] = img
        plt.close()

    def create_hdd_line_plot(self, x: list, y: list, key: str, title: str):
        # sns.set_theme(style="darkgrid")
        fig, ax1 = plt.subplots(figsize=(23, 3))
        ax1.set_ylabel("R/W Count")
        ax1.plot(x, y[0], c="g", marker="o", label="Read Count")
        ax1.plot(x, y[1], c="b", marker="o", label="Write Count")

        ax2 = ax1.twinx()
        ax2.set_ylabel("R/W Times")
        ax2.plot(x, y[2], c="r", ls="--", label="Read Time")
        ax2.plot(x, y[3], color="orange", ls="--", label="Write Count")
        fig.legend()

        fig.suptitle(title, fontsize=18)

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        img = f"data:image/png;base64,{data}"
        self.figures[key] = img
        plt.close()

    def create_net_line_plot(self, x: list, y: list, key: str, title: str):
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots(figsize=(23, 3))
        plt.title(title, fontsize=18)

        sns.lineplot(x=x, y=y[0], color="purple", label="Outbound")
        sns.lineplot(x=x, y=y[1], color="orange", label="Inbound")
        fig.legend()

        # plt.show()

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        img = f"data:image/png;base64,{data}"
        self.figures[key] = img
        plt.close()
