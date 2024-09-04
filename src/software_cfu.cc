#include <stdint.h>
#include "software_cfu.h"

uint32_t software_cfu(int funct3, int funct7, uint32_t rs1, uint32_t rs2) {
	if (funct3 == 0) {
		return rs1 + rs2;
	}
	return rs1;
}
