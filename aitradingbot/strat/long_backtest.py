import pickle
from os import remove
from os.path import exists
from time import perf_counter
from time import gmtime, strftime
from quantfreedom.backtesters import run_df_backtest
from quantfreedom.core.enums import FootprintCandlesTuple

from ema_cross import Long_Strat

if __name__ == "__main__":
    start_func = perf_counter()

    dbs_path = "C:/Users/gyama/TradingBot/aitradingbot/"
    bt_results_path = dbs_path + "bt_results/btr_long.h5"

    if exists(bt_results_path):
        remove(bt_results_path)

    print("loading candles")
    start = perf_counter()
    with open(dbs_path + "oct_dec_candles.pkl", "rb") as f:
        candles: FootprintCandlesTuple = pickle.load(f)
    
    end = perf_counter()
    print(strftime("%M:%S candles", gmtime(int(end - start))))

    backtest_results = run_df_backtest(
        candles=candles,
        strategy=Long_Strat,
        threads=8,
        step_by=4
    )

    print("\n" + "Backtest results done now saving to hdf5")
    backtest_results.to_hdf(
        path_or_buf=bt_results_path,
        key="backtest_results",
        mode="w"
    )

    end = perf_counter()
    print(strftime("\n" + "It took %M mins and %S seconds to complete the backtest", gmtime(int(end - start))))