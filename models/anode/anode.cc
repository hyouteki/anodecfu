#include <stdio.h>
#include "models/anode/anode.h"
#include "models/anode/models/arson_of_cnn_model.h"
#include "models/anode/models/arson_of_cnnlstm_model.h"
#include "models/anode/models/explosion_of_cnnlstm_model.h"
#include "models/anode/models/arson_cnn3dlstm_model.h"
#include "menu.h"
#include "tflite.h"

extern "C" {
#include "fb_util.h"
}

typedef enum {
	Anode_Model_Arson_OfCnnLstm,
	Anode_Model_Arson_OfCnn,
	Anode_Model_Explosion_OfCnnLstm,
	Anode_Model_Arson_Cnn3DLstm,
} Anode_ModelKind;

static int8_t MODEL_LOADED = 0;
static Anode_ModelKind SELECT_MODEL_KIND = Anode_Model_Arson_OfCnn;

static void Anode_Model_Load(Anode_ModelKind model_kind) {
	if (SELECT_MODEL_KIND == model_kind && MODEL_LOADED) return;
	switch (model_kind) {
	case Anode_Model_Arson_OfCnn:
		tflite_load_model(arson_of_cnn_tflite, arson_of_cnn_tflite_len);
		break;
	case Anode_Model_Arson_OfCnnLstm:
		tflite_load_model(arson_of_cnnlstm_tflite, arson_of_cnnlstm_tflite_len);
		break;
	case Anode_Model_Explosion_OfCnnLstm:
		tflite_load_model(explosion_of_cnnlstm_tflite, explosion_of_cnnlstm_tflite_len);
		break;
	case Anode_Model_Arson_Cnn3DLstm:
		tflite_load_model(arson_cnn3dlstm_tflite, arson_cnn3dlstm_tflite_len);
		break;
	default:
		printf("error: invalid model kind provided '%d'\n", model_kind);
		return;
	}
    MODEL_LOADED = 1;
    SELECT_MODEL_KIND = model_kind;
}

static void Anode_Model_Set_Arson_OfCnn() {
    Anode_Model_Load(Anode_Model_Arson_OfCnn);
}

static void Anode_Model_Set_Arson_OfCnnLstm() {
    Anode_Model_Load(Anode_Model_Arson_OfCnnLstm);
}

static void Anode_Model_Set_Explosion_OfCnnLstm() {
    Anode_Model_Load(Anode_Model_Explosion_OfCnnLstm);
}

static void Anode_Model_Set_Arson_Cnn3DLstm() {
    Anode_Model_Load(Anode_Model_Arson_Cnn3DLstm);
}

static int32_t Anode_Model_TestHelper() {
    if (!MODEL_LOADED) {
		printf("error: model not selected; select a model first\n");
		return -1;
	}
	printf("info: running model test");
	tflite_classify();
	int8_t* output = tflite_get_output();
	return output[1] - output[0];
}

static void Anode_Model_Test() {
	tflite_set_input_zeros();
	Anode_Model_TestHelper();
}

static struct Menu MENU = {
    "Anode options",
    "anode",
    {
        MENU_ITEM('1', "Select model 'arson_of_cnn'", Anode_Model_Set_Arson_OfCnn),
        MENU_ITEM('2', "Select model 'arson_of_cnnlstm'", Anode_Model_Set_Arson_OfCnnLstm),
        MENU_ITEM('3', "Select model 'explosion_of_cnnlstm'",
				  Anode_Model_Set_Explosion_OfCnnLstm),
		MENU_ITEM('4', "Select model 'arson_cnn3dlstm'", Anode_Model_Set_Arson_Cnn3DLstm),
        MENU_ITEM('t', "Test selected model", Anode_Model_Test),
        MENU_END,
    },
};

void Anode_Menu() {
	menu_run(&MENU);
}
