python3 cli.py \
	parameters-adjusment-ga \
	--ode SIRS \
	--bounds 0.01-1.0/0.01-1.0/0.01-1.0\
	--initial-condition 950 50 0 \
	--experimental-data .local/SIRS_experimental_data.csv \
	--G 5 \
	--P 6 \
	--mutation 0.3 \
	--tf 10 \
	--dt 0.01 \
	--output-file .local/sirs_ga.parameters

python3 cli.py \
	execute-ode-simulation \
	--ode SIRS \
	--initial-condition 950 50 0 \
	--parameters 0.3 0.1 0.8 \
	--solver solve_ivp \
	--tf 10 \
	--dt 0.01 | python3 cli.py \
	plot-csv \
	--output-file .local/plot.png


