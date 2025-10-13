import numpy as np
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline

def rf_tree_depth_est(given_preproc, train_data, train_targ, val_data, val_targ, mintrees=10, maxtrees=300, mindepth=5, maxdepth=40, max_iter=8):
    # This is the set where the best parameters are gathered
    final = []
    # Count for higher and lower paths chosen to help choose initial trees/depths
    highcount=[0,0]
    lowcount=[0,0]

    for i in range(max_iter):
        # the search is restricted on every iteration
        # if the low path is "better" during the test the new range is (mintrees, (mintrees+maxtrees)/2) (vice versa)
        # the words high and low are used to avoid confusion with min and max
        low_trees = int(mintrees + (maxtrees - mintrees)*(0.25))
        high_trees = int(mintrees + (maxtrees - mintrees)*0.75)
        low_depth = int(mindepth + (maxdepth - mindepth)*0.25)
        high_depth = int(mindepth + (maxdepth - mindepth) * 0.75)

        # these parameters are used in the inner iteration
        tests= [(low_trees, low_depth),(low_trees, high_depth),
            (high_trees, low_depth),(high_trees, high_depth)]
        
        results_for_tests = []
        k=i
        print(f"iteration number: {i}\n")
        for t, d in tests:
            # no overfitting by using k for the random state.
            # t=trees and d=depth for the particular test
            model = Pipeline(steps=[('preprocessor', given_preproc), 
                                    ('regressor',RandomForestRegressor(
                                                        n_estimators=t,
                                                        max_depth=d,
                                                        random_state=i,
                                                        n_jobs=-1))])
            model.fit(train_data, train_targ)
            prediction = model.predict(val_data)
            rmse = np.sqrt(mean_squared_error(val_targ,prediction))
            results_for_tests.append((rmse, t, d))
            print(f"Subiter: {i}.{k-i}, rmse: {rmse}")
            k+=1

        # the best values are purely based on which produced the best (smallest) rmse
        best_rmse, best_t, best_d = min(results_for_tests, key=lambda x: x[0])
        final.append((best_rmse, best_t, best_d))

        if best_t < (mintrees+maxtrees)/2:
            maxtrees=(mintrees+maxtrees)/2
            lowcount[0]+=1
            print("\nLower-trees route chosen\n")
        else:
            mintrees=(mintrees+maxtrees)/2
            highcount[0]+=1
            print("Higher-trees route chosen\n")
        if best_d < (mindepth+maxdepth)/2:
            maxdepth=(mindepth+maxdepth)/2
            lowcount[1]+=1
            print("Lower-depth route chosen\n")
        else:
            mindepth=(mindepth+maxdepth)/2
            highcount[1]+=1
            print("Higher-depth route chosen\n\n")
        
        if (maxtrees-mintrees <= 10) and (maxdepth-mindepth <= 3):
            break
    
    # the final parameters are chosen based also on the number of trees and amount of depth. Smaller values are preferred.
    best_rmse, best_t, best_d = min(final, key=lambda x: x[0] / (1 + 1 / math.log(x[1] * x[2] + 1)))
    print(f"Low-route count (trees) {lowcount[0]}\nHigh-route count (trees) {highcount[0]}\nLow-route count (depth) {lowcount[1]}\nHigh-route count (depth) {highcount[1]}")
    print(f'Final rmse: {best_rmse}\nEstimation for trees: {best_t}\nEstimation for depth: {best_d}')
    return (best_rmse, best_t, best_d)

