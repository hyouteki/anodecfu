all: mnist_model.h

%_model.h: %.tflite
	@echo "generating '$@'"
	@xxd -i $< > $@
