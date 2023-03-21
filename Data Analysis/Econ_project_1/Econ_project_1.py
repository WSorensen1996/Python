import pandas as pd 
import numpy as np
from numpy import linalg as la
from tabulate import tabulate
from scipy.stats import chi2

def estimate( 
        y: np.ndarray, x: np.ndarray, transform='', t:int=None
    ) -> list:
    """Uses the provided estimator (mostly OLS for now, and therefore we do 
    not need to provide the estimator) to perform a regression of y on x, 
    and provides all other necessary statistics such as standard errors, 
    t-values etc.  

    Args:
        >> y (np.ndarray): Dependent variable (Needs to have shape 2D shape)
        >> x (np.ndarray): Independent variable (Needs to have shape 2D shape)
        >> transform (str, optional): Defaults to ''. If the data is 
        transformed in any way, the following transformations are allowed:
            '': No transformations
            'fd': First-difference
            'be': Between transformation
            'fe': Within transformation
            're': Random effects estimation.
        >>t (int, optional): If panel data, t is the number of time periods in
        the panel, and is used for estimating the variance. Defaults to None.

    Returns:
        list: Returns a dictionary with the following variables:
        'b_hat', 'se', 'sigma2', 't_values', 'R2', 'cov'
    """
    
    b_hat = est_ols(y, x)  # Estimated coefficients
    residual = y - x@b_hat  # Calculated residuals
    SSR = residual.T@residual  # Sum of squared residuals
    SST = (y - np.mean(y)).T@(y - np.mean(y))  # Total sum of squares
    R2 = 1 - SSR/SST

    sigma2, cov, se = variance(transform, SSR, x, t)
    t_values = b_hat/se
    
    names = ['b_hat', 'se', 'sigma2', 't_values', 'R2', 'cov']
    results = [b_hat, se, sigma2, t_values, R2, cov]
    return dict(zip(names, results))
    
def est_ols( y: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Estimates y on x by ordinary least squares, returns coefficents

    Args:
        >> y (np.ndarray): Dependent variable (Needs to have shape 2D shape)
        >> x (np.ndarray): Independent variable (Needs to have shape 2D shape)

    Returns:
        np.array: Estimated beta coefficients.
    """
    return la.inv(x.T@x)@(x.T@y)

def variance( 
        transform: str, 
        SSR: float, 
        x: np.ndarray, 
        t: int
    ) -> tuple:
    """Calculates the covariance and standard errors from the OLS
    estimation.

    Args:
        >> transform (str): Defaults to ''. If the data is transformed in 
        any way, the following transformations are allowed:
            '': No transformations
            'fd': First-difference
            'be': Between transformation
            'fe': Within transformation
            're': Random effects estimation
        >> SSR (float): Sum of squared residuals
        >> x (np.ndarray): Dependent variables from regression
        >> t (int): The number of time periods in x.

    Raises:
        Exception: If invalid transformation is provided, returns
        an error.

    Returns:
        tuple: Returns the error variance (mean square error), 
        covariance matrix and standard errors.
    """

    # Store n and k, used for DF adjustments.
    k = x.shape[1]
    if transform in ('', 'fd', 'be'):
        n = x.shape[0]
    else:
        n = x.shape[0]/t

    # Calculate sigma2
    if transform in ('', 'fd', 'be'):
        sigma2 = (np.array(SSR/(n - k)))
    elif transform.lower() == 'fe':
        sigma2 = np.array(SSR/(n * (t - 1) - k))
    elif transform.lower() == 're':
        sigma2 = np.array(SSR/(t * n - k))
    else:
        raise Exception('Invalid transform provided.')
    
    cov = sigma2*la.inv(x.T@x)
    se = np.sqrt(cov.diagonal()).reshape(-1, 1)
    return sigma2, cov, se

def print_table(
        labels: tuple,
        results: dict,
        headers=["", "Beta", "Se", "t-values"],
        title="Results",
        _lambda:float=None,
        **kwargs
    ) -> None:
    """Prints a nice looking table, must at least have coefficients, 
    standard errors and t-values. The number of coefficients must be the
    same length as the labels.

    Args:
        >> labels (tuple): Touple with first a label for y, and then a list of 
        labels for x.
        >> results (dict): The results from a regression. Needs to be in a 
        dictionary with at least the following keys:
            'b_hat', 'se', 't_values', 'R2', 'sigma2'
        >> headers (list, optional): Column headers. Defaults to 
        ["", "Beta", "Se", "t-values"].
        >> title (str, optional): Table title. Defaults to "Results".
        _lambda (float, optional): Only used with Random effects. 
        Defaults to None.
    """
    
    # Unpack the labels
    label_y, label_x = labels
    
    # Create table, using the label for x to get a variable's coefficient,
    # standard error and t_value.
    table = []
    for i, name in enumerate(label_x):
        row = [
            name, 
            results.get('b_hat')[i], 
            results.get('se')[i], 
            results.get('t_values')[i]
        ]
        table.append(row)
    
    # Print the table
    print(title)
    print(f"Dependent variable: {label_y}\n")
    print(tabulate(table, headers, **kwargs))
    
    # Print extra statistics of the model.
    print(f"R\u00b2 = {results.get('R2').item():.3f}")
    print(f"\u03C3\u00b2 = {results.get('sigma2').item():.3f}")
    if _lambda: 
        print(f'\u03bb = {_lambda.item():.3f}')

def perm( Q_T: np.ndarray, A: np.ndarray) -> np.ndarray:
    """Takes a transformation matrix and performs the transformation on 
    the given vector or matrix.

    Args:
        Q_T (np.ndarray): The transformation matrix. Needs to have the same
        dimensions as number of years a person is in the sample.
        
        A (np.ndarray): The vector or matrix that is to be transformed. Has
        to be a 2d array.

    Returns:
        np.array: Returns the transformed vector or matrix.
    """
    # We can infer t from the shape of the transformation matrix.
    M,T = Q_T.shape 
    N = int(A.shape[0]/T)
    K = A.shape[1]

    # initialize output 
    Z = np.empty((M*N, K))
    
    for i in range(N): 
        ii_A = slice(i*T, (i+1)*T)
        ii_Z = slice(i*M, (i+1)*M)
        Z[ii_Z, :] = Q_T @ A[ii_A, :]

    return Z

def demeaning_matrix(t):
    Q_T = np.eye(t) - np.tile(1/t, (t, t))
    return Q_T

def check_rank(x):
    rank = la.matrix_rank(x) 
    print(f'Rank of demeaned x: {rank}')
    lambdas, V = la.eig(x.T@x)
    np.set_printoptions(suppress=True)  # This is just to print nicely.
    eigenvalue = lambdas.round(decimals=0)
    print(f'Eigenvalues of within-transformed x: {eigenvalue}')
    return rank, eigenvalue 

def fd_matrix(t):
    D_T = np.eye(t) - np.eye(t, k=-1)
    D_T = D_T[1:]
    return D_T

def serial_corr(y, x, t, year, firstyear, sndyear):
    b_hat = est_ols(y, x)
    e = y - x@b_hat
    
    # Create a lag to estimate the error on.
    L_T = np.eye(t, k=-1)
    L_T = L_T[1:]

    e_l = perm(L_T, e)

    # We then need to remove the first obs for every person again.
    reduced_year = year[year != firstyear]
    e = e[reduced_year != sndyear]
    
    return estimate(e, e_l)

def exogeneity_test(x, y, t, last_year, type):
    # Create lead
    F_T = np.eye(t, k=1)
    F_T = F_T[:-1]

    ##lead 
    lcap_lead = perm(F_T, x[:,1].reshape(-1,1)) # 1 = col  ############### 
    lemp_lead = perm(F_T, x[:,0].reshape(-1,1)) # 0 = col  ############### 

    # Collect variables to test for exogeneity
    x_exo = x[year != last_year]
    x_exo = np.hstack((x_exo, lcap_lead, lemp_lead))
    y_exo = y[year != last_year]

    if type.lower() == "fe": 
        # Within transform the data
        Q_T = demeaning_matrix(t - 1)
    if type.lower() == "fd": 
        Q_T = fd_matrix(t - 1)

    yw_exo = perm(Q_T, y_exo)
    xw_exo = perm(Q_T, x_exo)
    xw_exo = xw_exo[:, 1:] # fjerne konstant ###############

    label_exo = label_x 
    n = y.size/t
    # Estimate model
    exo_test = estimate(
        yw_exo, xw_exo, t=t - 1, transform = type
    )
    # Adjust sigma2 since

    print_table((label_y, label_exo), exo_test, title='Exogeneity test', floatfmt='.4f')

def mean_matrix(t):
    return np.tile(1/t, (1, t))

def print_h_test(fe_result, re_result, hat_diff, p_val):
    table = []
    for i in range(len(hat_diff)):
        row = [
            fe_result['b_hat'][i], re_result['b_hat'][i], hat_diff[i]
        ]
        table.append(row)

    print(tabulate(
        table, headers=['b_fe', 'b_re', 'b_diff'], floatfmt='.4f'
        ))
    print(f'\nThe Hausman test statistic is: {H.item():.2f}, with p-value: {p_val:.2f}.')


if __name__ == "__main__": 

    dat = pd.read_csv('firms.csv')
    dat.year.unique()
    id_array = dat.firmid.values

    year = dat.year.values
    unique_id = np.unique(id_array, return_counts=True)
    n = unique_id[0].size
    t = int(unique_id[1].mean())

    y = dat.ldsa.values
    x = np.array([
        dat.lcap.values,
        dat.lemp.values
    ])

    label_y = 'ldsa'
    label_x = [
        "lcap",
        "lemp"
    ]

    ### Pooled OLS  ######################################################################
    ols_result = estimate(y, x.T)
    print_table( (label_y, label_x), ols_result, title="Pooled OLS", floatfmt='.4f' )
    print("\n\n")

    ### FE ######################################################################
    # Assumption made: E[v_it·x_it ]=E[c_i·x_it ]+E[u_it·x_it ]=0
    Q_T = demeaning_matrix(t)

    y_demean = perm(Q_T, y.reshape(-1,1))
    x_demean = perm(Q_T, x.T)

    #Making sure X has full rank 
    print("Full rank:", (check_rank(x_demean)[0]==len(x)))

    #Estimating FE:  ######################################################################
    fe_result = estimate( y_demean, x_demean, transform='fe', t=t )
    print_table((label_y, label_x), fe_result, title='FE regression', floatfmt='.4f' )
    print("\n\n")

    ### FD 
    # Transform the data.
    D_T = fd_matrix(t)
    y_diff = perm(D_T, y.reshape(-1,1))
    x_diff = perm(D_T, x.T)

    # Again, check rank condition.
    print("Full rank:", (check_rank(x_demean)[0]==len(x)))

    #Estimating FD: ######################################################################
    fd_result = estimate(y_diff, x_diff,transform='fd', t=t)
    print_table((label_y, label_x), fd_result, title='FD regression', floatfmt='.4f')
    print("\n\n")

    ### Comparing FE and FD ######################################################################
    firstyear = year[0] # For removing first year 
    sndyear = year[1]   # For removing second year 
    corr_result = serial_corr(y_diff, x_diff, t-1, year, firstyear, sndyear)
    label_ye = 'OLS residual, e\u1d62\u209c'
    label_e = ['e\u1d62\u209c\u208B\u2081']
    title = 'Serial Correlation'
    print_table((label_ye, label_e), corr_result, title='Serial Correlation', floatfmt='.4f')

    lastyear = year[-1] 

    ### Exogeneity test ######################################################################
    print("\nComparing FE and FD:")
    exogeneity_test(x.T, y.reshape(-1,1), t, lastyear, "fe")
    print("\n")
    exogeneity_test(x.T, y.reshape(-1,1), t, lastyear, "fd")

    ## RE estimatior  ###################################################################### 
    P_T = mean_matrix(t)
    y_mean = perm(P_T, y.reshape(-1,1))
    x_mean = perm(P_T, x.T)

    print("\n\n")
    be_result = estimate( y_mean, x_mean, transform='be')
    print_table(
        labels=(label_y, label_x), results=be_result, title='BE',
        floatfmt=['', '.4f', '.4f', '.2f'] )

    sigma_u = fe_result['sigma2']
    sigma_c = be_result['sigma2'] - sigma_u/t
    _lambda = 1 - np.sqrt(sigma_u/(sigma_u + t*sigma_c))
    print("\nLambda: ",_lambda)

    print("\n\n")
    C_t = np.eye(t) - _lambda*mean_matrix(t)
    x_re = perm(C_t, x.T)
    y_re = perm(C_t, y.reshape(-1,1))

    re_result = estimate(
        y_re, x_re, transform='re', t=t
    )
    print_table(
        labels=(label_y, label_x), results=re_result, _lambda=_lambda,
        title='RE',
        floatfmt=['', '.3f', '.4f', '.2f']
    )

    ## Hauseman test ###################################################################### 
    b_re = re_result['b_hat']

    hat_diff = fe_result['b_hat'] - b_re  # The differences in beta hat
    cov_re = re_result['cov']

    cov_diff = fe_result['cov'] - cov_re  # The difference in covariances
    H = hat_diff.T@la.inv(cov_diff)@hat_diff  # The Hausman test value

    # This calculates the p-value of the Hausman test.
    p_val = chi2.sf(H.item(), 4)

    # First calculate the covar matrices.
    # Remember to remove the FE time invarant regressors from RE
    hat_diff = fe_result['b_hat'] - re_result['b_hat']
    cov_diff = la.inv(fe_result['cov'] - re_result['cov'])
    H = hat_diff.T@(cov_diff@hat_diff)
    # This takes the chi2 value, and then DF.
    p_val = chi2.sf(H.item(), hat_diff.size)

    # This code takes the results that you have made, and prints a nice looking table.
    print_h_test(fe_result, re_result, hat_diff, p_val)

    R = np.array([1,1])
    r = 1
    significans_lvl = 0.05

    W = (R@ols_result["b_hat"]-r).T * ((R * ols_result["sigma2"] @ R.T)**-1) * (R@ols_result["b_hat"]-r)
    print("Wald test value: ", W)
    print("We can reject H0: ", W>(1-significans_lvl))





