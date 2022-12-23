from collections import deque
from logging import getLogger
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty
from time import sleep
from typing import Callable, Tuple, Union, List

try:
    from matplotlib import pyplot as plt
    from matplotlib.animation import FuncAnimation
    _MATPLOTLIB = True
except ImportError:
    print("WARNING: Could not import matplotlib. LivePlot will not work correctly.")
    _MATPLOTLIB = False


MetricFuncRet = Tuple[Union[int, float], List[Tuple[str, Union[int, float]]]]
MetricFunc = Callable[[...], MetricFuncRet]


class LivePlot(Process):

    def __init__(
        self,
        metric_fn: MetricFunc,
        maxplot=500,
        maxqueue=1000000,
        interval=500,
        disable_matplotlib=False,
    ) -> None:
        super().__init__()
        self._queue = Queue(maxsize=maxqueue)
        self._xvals = deque(maxlen=maxplot)
        self._interval = interval
        self._maxplot = maxplot
        self._mf = metric_fn
        self._series = {}
        self._with_matplotlib = (not disable_matplotlib) and _MATPLOTLIB
        self._log = getLogger(self.__class__.__name__)

    def run(self) -> None:
        if self._with_matplotlib:
            self._run_with_matplotlib()
        else:
            self._log.warning("Matplotlib is disabled or not installed.")
            self._run_without_matplotlib()

    def _run_without_matplotlib(self):
        while True:
            try:
                data = self._queue.get_nowait()
            except Empty:
                sleep(0)
            else:
                self._add_metrics(*data)
                while self._xvals:
                    xval = self._xvals.popleft()
                    self._log.info(xval)
                    for name, queue in self._series.items():
                        self._log.info("- %s: %s", name, queue.popleft())

    def _run_with_matplotlib(self):

        plt.style.use("fivethirtyeight")

        def animate(i):
            while not self._queue.empty():
                data = self._queue.get_nowait()
                self._add_metrics(*data)

            plt.cla()
            for k, v in self._series.items():
                plt.plot(self._xvals, v, label=k)
            plt.legend(loc="upper left")
            plt.tight_layout()

        ani = FuncAnimation(plt.gcf(), animate, interval=self._interval)
        plt.show()

    def _add_metrics(self, args, kwargs):
        xval, metrics = self._mf(*args, **kwargs)
        self._xvals.append(xval)
        for name, value in metrics:
            self._series.setdefault(name, deque(maxlen=self._maxplot)).append(value)

    def enqueue(self, *args, **kwargs) -> None:
        self._queue.put((args, kwargs))
