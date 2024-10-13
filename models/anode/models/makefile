all: arson_of_cnn_model.h arson_of_cnnlstm_model.h explosion_of_cnnlstm_model.h arson_cnn3dlstm_model.h

%_model.h: %.tflite
	@echo "generating '$@'"
	@xxd -i $< > $@
