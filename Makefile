CC=clang

all: task1 task1_asan corner_case_stress.so test_task1
	@echo "DONE"

task1: task1.c
	$(CC) -o $@ $^

task1_asan: task1.c
	$(CC) -fsanitize=address -Wl,--no-export-dynamic -o $@ $^ &> /dev/null

test_task1: 
	python3 -m unittest test_task1 -v

corner_case_stress.so: corner_case_stress.c
	$(CC) -shared -fPIC -o $@ $^

clean:
	rm -f task1 task1_asan corner_case_stress.so