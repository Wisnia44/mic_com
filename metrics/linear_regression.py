import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

plt.style.use("bmh")


def get_regression(x_1, y_1, x_2, y_2, proces_name, fig_num):
    plt.figure(fig_num)

    model_1 = LinearRegression().fit(x_1, y_1)
    a_1 = model_1.coef_[0]
    b_1 = model_1.intercept_
    y_1_pred = a_1 * x_1 + b_1

    plt.plot(x_1, y_1_pred, label="Choreografia", color="#348ABD")
    plt.scatter(x_1, y_1, color="#348ABD")
    plt.text(
        x_1[-1] - 1,
        y_1[-1],
        f"y = {a_1:.2f} * x + {b_1:.2f}",
        horizontalalignment="right",
        verticalalignment="center",
        color="#348ABD",
    )

    model_2 = LinearRegression().fit(x_2, y_2)
    a_2 = model_2.coef_[0]
    b_2 = model_2.intercept_
    y_2_pred = a_2 * x_2 + b_2

    plt.plot(x_2, y_2_pred, label="Orkiestracja", color="#A60628")
    plt.scatter(x_2, y_2, color="#A60628")
    plt.text(
        x_2[0] + 1,
        y_2[0],
        f"y = {a_2:.2f} * x + {b_2:.2f}",
        horizontalalignment="left",
        verticalalignment="center",
        color="#A60628",
    )

    plt.title(
        f"Model regresji liniowej dla procesu \n {proces_name} dla obu kompozycji"
    )
    plt.xlabel("Wartość obciążenia")
    plt.ylabel("Średni czas odpowiedzi [ms]")
    plt.legend()
    # plt.show()
    plt.savefig(f"img/{proces_name}")


load = np.asarray([10, 30, 50]).reshape((-1, 1))

ch_first_enter = np.asarray([986, 2759, 4250])
ch_again_enter = np.asarray([364, 970, 1594])
ch_exit = np.asarray([972, 2698, 4615])

or_first_enter = np.asarray([732, 2318, 3807])
or_again_enter = np.asarray([417, 1259, 1942])
or_exit = np.asarray([860, 2640, 4315])

ch_first_enter_model = LinearRegression().fit(load, ch_first_enter)
ch_first_enter_a = ch_first_enter_model.coef_[0]
ch_first_enter_b = ch_first_enter_model.intercept_

get_regression(load, ch_first_enter, load, or_first_enter, "pierwszego wejścia", 1)
get_regression(load, ch_again_enter, load, or_again_enter, "ponownego wejścia", 2)
get_regression(load, ch_exit, load, or_exit, "wyjścia", 3)
