if [ "$1" = "fit" ]; then
	echo "Running fitting with Genetic Algorithm ..."

	python3 fit.py ga \
			--experimental-data ./.local/experimental_data.csv \
			--tf 10 \
			--dt 0.01 \
			--y0 995 5 0 \
			--bounds 0.1-1.0/0.1-1.0/0.1-1.0 \
			--G 30 \
			--P 80 \
			--mutation 0.3 \
			--output-file ".local/ga.parameters" \
			| ./parse_fitting_stdout_to_csv.sh \
			| python3 plot_errors.py \
				--output-file ".local/ga_errors.png"

	echo "Running fitting with Differential Evolution ..."

	python3 fit.py de \
			--experimental-data ./.local/experimental_data.csv \
			--y0 995 5 0 \
			--bounds 0.1-1.0/0.1-1.0/0.1-1.0 \
			--mutation 0.3 \
			--recombination 0.5 \
			--maxiter 30 \
			--popsize 80 \
			--tf 10 \
			--dt 0.01 \
			--output-file ".local/de.parameters" \
			| ./parse_fitting_stdout_to_csv.sh \
			| python3 plot_errors.py \
				--output-file ".local/de_errors.png"
fi

xdg-open ".local/ga_errors.png"
xdg-open ".local/de_errors.png"

python3 simulate.py \
		--ode-params $(cat .local/ga.parameters | sed --expression "s/,/ /g") \
		--y0 995 5 0 \
		--tf 10 \
		--dt 0.01 \
		| python3 plot_simulation.py \
		--experimental-data ".local/experimental_data.csv" \
		--y0 995 5 0 \
		--output-file ".local/ga_best_params_simulation.png" && xdg-open ".local/ga_best_params_simulation.png"

python3 simulate.py \
		--ode-params $(cat .local/de.parameters | sed --expression "s/,/ /g") \
		--y0 995 5 0 \
		--tf 10 \
		--dt 0.01 \
		| python3 plot_simulation.py \
		--experimental-data ".local/experimental_data.csv" \
		--y0 995 5 0 \
		--output-file ".local/de_best_params_simulation.png" && xdg-open ".local/de_best_params_simulation.png"

# cp .local/*.png .local/*.parameters ~/Documents/Latex/IMC-TP4/assets/
