#include <stdio.h>

#include "liym/liym.h"

int main(int argc, char* argv[]) {
	if (argc > 3) {
		printf("Too many args\n");
		return -1;
	}

	if (argc < 3) {
		printf("Not enough args\n");
		return -1;
	}

	
	FILE *infile;
	struct liymParseResults parse = openLiymFromFile(atoi(argv[2]), argv[1], infile);
	// ^Struct containing pointers to arrays of data      ^Parse specified model

	if (parse.filetype == 0) {
		printf("Parse failed or model has no data\n");
	} else {
		printf("Got filetype %d back from liym parser\n", parse.filetype);
	}

	freeLiym(parse);

	struct liyaParseResults aparse = initLiyaStreamer("in/anim.liya", &infile);

	if (aparse.bonecount == 0) {
		printf("Parse failed or anim has no bones\n");
	} else {
		printf("Got %d bones back from liya parser\n", aparse.bonecount);
	}

	for(int i = 0; i < aparse.framecount; i++) {
		aparse = liyaStreamframe(aparse, infile);
	}


	freeLiya(aparse, infile);
}