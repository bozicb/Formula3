# This dictionary maps aggregate names to objects that calculate those aggregates 
aggregates ={ 'None' : agg.none_aggregate(),
              'mean' : agg.calc_mean(),
              'mean_status'  : agg.calc_my_mean(),
              'max'  : agg.calc_max(),
              'min'  : agg.calc_min(),
              'sum'  : agg.calc_sum(),
              'count': agg.calc_count(),
              'log'  : agg.calc_log(),
            }


