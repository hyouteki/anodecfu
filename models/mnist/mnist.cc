#include <stdio.h>
#include "models/mnist/mnist.h"
#include "models/mnist/mnist_model.h"
#include "menu.h"
#include "tflite.h"

extern "C" {
#include "fb_util.h"
}

static void mnist_init(void) {
	tflite_load_model(mnist_model_tflite, mnist_model_tflite_len);
}

static int32_t mnist_classify() {
	printf("Running mnist\n");
	tflite_classify();
	int8_t* output = tflite_get_output();
	return output[1] - output[0];
}

static void do_classify_zeros() {
	tflite_set_input_zeros();
	int32_t result = mnist_classify();
	printf("|  result: %ld\n", result);
}

static struct Menu MENU = {
    "Tests for mnist model",
    "mnist",
    {
        MENU_ITEM('1', "Run with zeros input", do_classify_zeros),
        MENU_END,
    },
};

void mnist_menu() {
	mnist_init();
	menu_run(&MENU);
}
