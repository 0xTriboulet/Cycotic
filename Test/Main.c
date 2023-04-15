// x86_64-w64-mingw32-gcc Main.c -o Poly.exe -masm=intel

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <windows.h>

void replaceBytes(void);
void other_function(void);

asm("startAddress:");
int main(void){
	// print count
	int i = 0;

	// test print
	printf("MAIN: PRINT %d\n", i++);
	printf("MAIN: PRINT %d\n", i++);
	
	// replace bytes
	replaceBytes();

	// test print
	printf("MAIN: PRINT %d\n", i++);
	printf("MAIN: PRINT %d\n", i++);
	
	other_function();

	return 0;
}

// other function used for testing
void other_function(void){

	int i = 0;
	
	printf("OTHER_FUNCTION: PRINT %d\n", i++);	
	printf("OTHER_FUNCTION: PRINT %d\n", i);	
	
}

// function that replaces target bytes
void replaceBytes() {
	// addreses
	PVOID startAddress = NULL;
	PVOID endAddress = NULL;
	
	// pattern of bytes our replaceBytes function is going to look for
	BYTE pattern[] = { 0x31, 0xC0, 0x31, 0xC0, 0x31, 0xC9, 0x31, 0xD2, 0x45, 0x31, 0xC0 };
	
	// pattern length
	size_t patternLen = sizeof(pattern);
	
	// get startAddress
	asm("lea %0, [rip+startAddress];"
	: "=r" (startAddress)
	::);
	
	// get endAddress
	asm("lea %0, [rip+endAddress];"
	: "=r" (endAddress)
	::);
	
	// size of our target patch area
	size_t remainingLen = endAddress - startAddress;
	uint8_t * currAddr = startAddress;

	// relative jump + 10 (0x0a) so we can jump over our junk instructions
	BYTE replacementBytes [11] = { 0xEB, 0x09 };

	// size of replacement

	size_t replacementLen = patternLen;

	
	BYTE random = 0;
	int j;
	
	// generate random bytes to replace our patternBytes
	for (j = 2 ; j < replacementLen; j++){
		asm("rdrand rax;"
		: "=r" (random)
		);
		replacementBytes[j] = random;
	}
			
	DWORD oldProtect = 0x0;
	
    while (remainingLen > 0) {

		// check if the current memory location matches the pattern
        if (memcmp(currAddr, pattern, patternLen) == 0) {

			// RWX permissions so we can overwrite our bytes
			VirtualProtect(currAddr, remainingLen, PAGE_EXECUTE_READWRITE, &oldProtect);
			
            // pattern match found, replace the bytes
            MoveMemory(currAddr, replacementBytes, replacementLen);
			
			// Restore permissions so we can overwrite our bytes
			VirtualProtect(currAddr, remainingLen, oldProtect, &oldProtect);
	
			if (*(currAddr+1) != 0x09){
				printf("ERROR COPYING MEMORY\n");
			}
			
            currAddr += replacementLen;
            remainingLen -= replacementLen;
			
        } else {
            // no match found, advance to the next byte
            currAddr++;
            remainingLen--;
        }
    }
}
asm("endAddress:");
