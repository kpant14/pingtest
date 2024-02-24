from ping3 import ping
import matplotlib.pyplot as plt
import datetime
from matplotlib.widgets import Button, TextBox


class Pingplot:

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.3)

        self.period = 1
        self.period_cache = 1
        self.site = "192.168.123.162"
        self.site_cache = "192.168.123.162"
        self.reset()

    def b_pause(self, event):
        self.paused = not self.paused

    def b_reset(self, event):
        self.reset()
        self.ax.clear()
        plt.draw()

    def b_dump(self, event):
        time = str(datetime.datetime.now())
        site = self.site

        csv_data = "time:," + time + "\nsite:," + site + "\n" + "ping (ms),time(s)\n"

        for i in range (0, len(self.ys)) :
            csv_data += str(self.ys[i]) + "," + str(self.xs[i]) + "\n"

        f = open('PingDump.csv', "w")
        f.write(csv_data)
        f.close()

    def reset(self):
        self.iter = 0
        self.xs = [0]
        self.ys = [0]
        self.paused = True

        self.period = self.period_cache
        self.site = self.site_cache

    def tb_siteinput(self, text):
        self.site_cache = text
        plt.draw()

    def tb_periodinput(self, text):
        try: self.period_cache = float(text)
        except: print("period must be a number")
        plt.draw()

    def data_append(self, event):
        if self.paused == False:
            self.iter += 1
            if self.iter % self.period == 0:
                self.iter = 0
                try: 
                    y = (ping(self.site, unit='ms', timeout = self.period))
                except:
                    y = self.period * 1000
                if y != None and y != False:
                    self.ys.append(y)
                else:
                    self.ys.append(self.period * 1000)
                x = len(self.xs) * self.period
                self.xs.append(x)

                self.ax.clear()
                self.ax.set(xlabel= 'time (s)', ylabel= 'ping (ms)', title= 'Ping with ' + self.site)
                self.ax.plot(self.xs, self.ys)
                print("ping data gotten: " + str(y) + " (ms) time: " + str(x))
                plt.draw()

x = Pingplot()

breset = Button(plt.axes([0.625, 0.15, 0.2, 0.075]), 'Restart')
bpause = Button(plt.axes([0.625, 0.05, 0.2, 0.075]), 'run/pause')
bdump = Button(plt.axes([0.412, 0.05, 0.2, 0.075]), 'dump')
tbsite = TextBox(plt.axes([0.2, 0.15, 0.2, 0.075]), 'site', initial=x.site)
tbperiod = TextBox(plt.axes([0.3, 0.05, 0.1, 0.075]), 'checking period (s)', initial=x.period)

breset.on_clicked(x.b_reset)
bpause.on_clicked(x.b_pause)
bdump.on_clicked(x.b_dump)
tbsite.on_submit(x.tb_siteinput)
tbperiod.on_submit(x.tb_periodinput)

timer = x.fig.canvas.new_timer(interval=x.period*1000)
timer.add_callback(x.data_append, x.ax)
timer.start()

plt.show()