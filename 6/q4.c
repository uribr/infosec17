#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>

int pid = 0x12345678;
#define SYSCALL_READ_ID 3
#define IS_DIRECTORY_ADDRESS 0x804878b
#define CHECK_IF_VIRUS_PLT_ADDRESS 0x0804a01c

int main(int argc, char **argv) 
{

    struct user_regs_struct regs;

    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }
        if(ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1)
    {
        perror("attach");
        return -1;
    }
    int status;
    waitpid(pid, &status, 0);
    if(WIFEXITED(status)) {return -1;} 
    while(1)
    {
        ptrace(PTRACE_SYSCALL, pid, NULL, NULL); //Stop at the read system call.
        waitpid(pid, &status, 0);
        if(WIFEXITED(status)) {return -1;} 
        ptrace(PTRACE_GETREGS, pid, NULL, &regs); // Get current registers.
        if(regs.orig_eax == SYSCALL_READ_ID)
        {
            regs.edx = 0; // Set the size of the file to 0.
            ptrace(PTRACE_SETREGS, pid, NULL, &regs); // Put registers back.
        }
    }
    return 0;
}
