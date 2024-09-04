#include <stdio.h>
#include "proj_menu.h"
#include "cfu.h"
#include "menu.h"

namespace {
	void do_hello_world(void) {
		puts("Hello World\n");
	}

	void do_exercise_cfu_op0(void) {
		puts("\nExercise CFU Op0 aka Mean\n");
		unsigned int a = 0, b = 0, cfu = 0, count = 0, \
			pass_count = 0, fail_count = 0;

		for (a = 0x00004567; a < 0xF8000000; a += 0x00212345) {
			for (b = 0x0000ba98; b < 0xFF000000; b += 0x00770077) {
				cfu = cfu_op0(0, a, b);
				if (cfu != a + b) {
					printf("[%4d] a: %08x b:%08x a+b=%08x "
						   "cfu=%08x FAIL\r\n",
						   count, a, b, a + b, cfu);
					fail_count++;
				} else {
					pass_count++;
				}
				count++;
			}
		}
		printf("\r\nPerformed %d comparisons, %d pass, "
			   "%d fail\r\n", count, pass_count, fail_count);
	}

	struct Menu MENU = {
		"Mean menu",
		"mean",
		{
			MENU_ITEM('0', "exercise cfu op0", do_exercise_cfu_op0),
			MENU_ITEM('h', "say Hello", do_hello_world),
			MENU_END,
		},
	};
};

extern "C" void do_proj_menu() {
	menu_run(&MENU);
}
