all: arson_of_cnn_model.h arson_of_cnnlstm_model.h

%_model.h: %.tflite
	@echo "generating '$@'"
	@xxd -i $< > $@
