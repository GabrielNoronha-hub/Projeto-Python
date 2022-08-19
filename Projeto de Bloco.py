import pygame, psutil, sys, cpuinfo, socket, getpass, platform, os, time, subprocess, nmap

# Criando a tela do sistema
largura_tela = 800
altura_tela = 600
info_cpu = cpuinfo.get_cpu_info()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Projeto de Bloco")
pygame.display.init()
pygame.font.init()
font = pygame.font.SysFont("arial", 19)

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
cinza = (120, 120, 120)
verde = (0, 255, 0)
vermelho = (255, 0, 0)
cinza_escuro = (50, 50, 50)

# Surfaces
sur_infocpu = pygame.surface.Surface((largura_tela, altura_tela/4))
sur_memoria = pygame.surface.Surface((largura_tela, altura_tela/4))
sur_cpu = pygame.surface.Surface((largura_tela, altura_tela/4))
sur_disco = pygame.surface.Surface((largura_tela, altura_tela/4))
sur_ip = pygame.surface.Surface((largura_tela, altura_tela/4))

def mostra_uso_memoria(x, y):
    memoria = psutil.virtual_memory()
    largura = largura_tela - 2 * 20
    pygame.draw.rect(sur_memoria, cinza_escuro, (20, 0, largura, 50))
    tela.blit(sur_memoria, (0, x))
    largura = largura * memoria.percent / 100
    pygame.draw.rect(sur_memoria, verde, (20, 0, largura, 50))
    tela.blit(sur_memoria, (0, x))
    total = round(memoria.total / (1024 * 1024 * 1024), 2)
    percentagem = memoria.percent
    texto_da_barra = (
        'Uso de Memória: {}% (Total: {} GB)'.format(percentagem, total))
    text = font.render(texto_da_barra, 1, branco)
    tela.blit(text, (20, y))
    

# Função para capturar o uso de CPU
def mostra_uso_cpu(s, l_cpu_percent, A, B, C, D, E):
    s.fill(preto)
    capacidade = psutil.cpu_percent(interval=1)
    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s.get_height() - 2 * y
    larg = (s.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s, C, (d, y + 20, larg, alt))
        pygame.draw.rect(s, D, (d, y + 20, larg, (1 - i / 100) * alt))
        d = d + larg + desl
    text = font.render("Uso de CPU por núcleo total: " +
                       str(capacidade) + "%", 1, E)
    s.blit(text, (20, A))
    tela.blit(s, (0, B))

# Função para mostrar os detalhes da cpu
def mostra_info_cpu(s, X):
    mostra_texto(s, "Nome:", "brand_raw", 10)
    mostra_texto(s, "Arquitetura:", "arch", 40)
    mostra_texto(s, "Palavra (bits):", "bits", 70)
    mostra_texto(s, "Frequência Total (MHz):", "freq_total", 110)
    mostra_texto(s, "Frequência de Uso (MHz): ", "freq", 130)
    mostra_texto(s, "Núcleos (físicos):", "nucleos", 150)
    mostra_texto(s, "Núcleos (lógicos):", "nucleos_logicos", 180)
    tela.blit(s, (10, X))
    s.fill(preto)

# Função para mostrar as infos da cpu
def mostra_texto(sur, nome, chave, pos_y):
    if chave == "freq":
        s = str(round(psutil.cpu_freq().current, 1))
    elif chave == "freq_total":
        s = str(round(psutil.cpu_freq().max, 2))
    elif chave == "nucleos":
        s = str(psutil.cpu_count())
        s = s + " (" + str(psutil.cpu_count(logical=False)) + ")"
    elif chave == "nucleos_logicos":
        s = str(psutil.cpu_count())
        s = s + " (" + str(psutil.cpu_count(logical=True)) + ")"
    else:
        s = str(info_cpu[chave])
    
    texto = nome + " " + s
    text = font.render(texto, True, branco)
    sur.blit(text, (10, pos_y))

# Função para capturar o uso do disco
def mostra_uso_disco(x, y):
    disco = psutil.disk_usage('.')
    largura = largura_tela - 2 * 20
    pygame.draw.rect(sur_disco, cinza_escuro, (20, 5, largura, 50))
    tela.blit(sur_disco, (0, x))
    largura = largura * disco.percent / 100
    pygame.draw.rect(sur_disco, verde, (20, 5, largura, 50))
    tela.blit(sur_disco, (0, x))
    total = round(disco.total / (1024 * 1024 * 1024), 2)
    percentagem = disco.percent
    texto_da_barra = (
        'Uso de Disco: {}% (Total: {} GB)'.format(percentagem, total))
    text = font.render(texto_da_barra, 1, branco)
    tela.blit(text, (x, y))

# Captura o nome da Máquina
def nome_maquina(x, y):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    texto_barra = "Nome da Máquina: " + str(hostname)
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (x, y))

def usuario(x,y):
    user = getpass.getuser()
    texto_barra =  "Usuário: " + str(user)
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (x, y))
    
def so(x,y):
    sistema = platform.system()
    texto_barra = "Sistema Operacional: " + str(sistema)
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (x, y))

# Captura IP interno
def ip_interno(x,y):
    hostname = socket.gethostname()
    ip_interno = socket.gethostbyname(hostname)
    texto_barra = "IP da máquina: "+ (ip_interno)
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (x, y))
    
def pid(x, y):
    lista = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        i = (proc.info)
        lista.append(i)
    
    height = y
    for linha in lista:
        if height == y:
            texto_barra = "PROCESSOS"
        elif height<500:
            texto_barra = "PID: " + str(linha['pid']) + " Processo: " + str(linha['name']) + " Usuário: " + str(linha ['username'])
        else: texto_barra = ''

        text = font.render(texto_barra, 1, branco)
        tela.blit(text, (x, height))
        height = height + 20

def arquivos(x,y):
    
    lista = os.listdir()

    dic = {}
    titulo = '{:11}'.format("Tamanho") # 10 Caracteres + 1 de espaço
    titulo = titulo + '{:27}'.format("Data de Modificação")
    titulo = titulo + '{:27}'.format("Data de criação")
    titulo = titulo + "Nome"
    #print(titulo)
    dic["header"] = "ARQUIVOS"
    dic["titulo"] = titulo

    for i in lista:
        if os.path.isfile(i):
            dicFile = []
            dicFile.append(os.stat(i).st_size)  # Tamanho
            dicFile.append(time.ctime(os.stat(i).st_atime)) # Tempo de criação 
            dicFile.append(time.ctime(os.stat(i).st_mtime)) # Tempo 
            dic[i] = dicFile

    for i in dic:
        if i == "header":
            text = font.render(dic[i], 1, branco)
            tela.blit(text, (x, y))
            y+=20
            continue
        if i == "titulo":
            text = font.render(dic[i], 1, branco)
            tela.blit(text, (x, y))
            y+=20
            continue
        kb = dic[i][0]/1000
        tamanho = '{:10}'.format(str('{:.2f}'.format(kb)+' KB'))
        dataMod = dic[i][1]
        dataCri = dic[i][2]
        result = ('{:11}'.format(tamanho) + '{:27}'.format(dataMod) + '{:27}'.format(dataCri) + i)
        text = font.render(result, 1, branco)
        tela.blit(text, (x, y))
        y+=20


def retorna_codigo_ping(hostname):
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]
    
    ret_cod = subprocess.call(args,
                            stdout=open(os.devnull, 'w'),
                            stderr=open(os.devnull, 'w'))
    return ret_cod

def verifica_hosts(base_ip):
    """Verifica todos os host com a base_ip entre 1 e 255 retorna uma lista com todos os host que tiveram resposta 0 (ativo)"""
    print("Mapeando\r")
    host_validos = []
    return_codes = dict()
    for i in range(1, 255):
    
        return_codes[base_ip + '{0}'.format(i)] =   retorna_codigo_ping(base_ip + '{0}'.format(i))
        if i %20 ==0:
            print(".", end = "")
        if        return_codes[base_ip + '{0}'.format(i)] == 0:
            host_validos.append(base_ip + '{0}'.format(i))
    print("\nMapping ready...")

    return host_validos

def maquinas_subrede(x, y, maquinas):
    nm = nmap.PortScanner()
    if len(maquinas)>0:
        for i in maquinas:
            try:
                nm.scan(i)
                result = "O IP", i, "possui o nome", nm[i].hostname()
                text = font.render(result, 1, branco)
                tela.blit(text, (x, y))
            except:
                pass
    else:
        result = 'Nenhuma outra máquina encontrada'
        text = font.render(result, 1, branco)
        tela.blit(text, (x, y))

def postas_subrede(x, y, maquinas):
        nm = nmap.PortScanner()
        if len(maquinas)>0:
            for host in maquinas:
                nm.scan(host)
                hostname = nm[host].hostname()
                for proto in nm[host].all_protocols():
                    print('----------')
                    print('Protocolo : %s' % proto)

                    lport = nm[host][proto].keys()
                    for port in lport:
                        result = 'Porta: %s\t Estado: %s' % (port, nm[host][proto][port]['state'])
                        text = font.render(result, 1, branco)
                        tela.blit(text, (x, y))
        else:
            result = 'Nenhuma outra máquina encontrada'
            text = font.render(result, 1, branco)
            tela.blit(text, (x, y))

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
maquinas = verifica_hosts(ip)

def slide():
    tela_2 = tela_3 = tela_4 = tela_5 = tela_6 = tela_7 = tela_8 = False
    tela_1 = True

    while tela_1:
        tela.fill(preto)
        nome_maquina(20, 30)
        usuario(20, 50)
        so(20,70)
        ip_interno(20, 90)
        pid(20,130)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_1 = False
                    tela_2 = True
                if event.key == pygame.K_LEFT:
                    tela_1 = False
                    tela_8 = True
                if event.key == pygame.K_SPACE:
                    tela_1 = False
                    tela_6 = True
                    
                    
    while tela_2:
        tela.fill(preto)
        mostra_uso_memoria(310, 280)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_2 = False
                    tela_3 = True
                if event.key == pygame.K_LEFT:
                    tela_2 = False
                    tela_1 = True
                if event.key == pygame.K_SPACE:
                    tela_2 = False
                    tela_6 = True

    while tela_3:
        tela.fill(preto)
        mostra_uso_cpu(sur_cpu, psutil.cpu_percent(
            percpu=True), 5, 200, verde, cinza_escuro, branco)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_3 = False
                    tela_4 = True
                if event.key == pygame.K_LEFT:
                    tela_3 = False
                    tela_2 = True
                if event.key == pygame.K_SPACE:
                    tela_3 = False
                    tela_6 = True
                    

    while tela_4:
        tela.fill(preto)
        mostra_info_cpu(sur_infocpu, 45)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_4 = False
                    tela_5 = True
                if event.key == pygame.K_LEFT:
                    tela_4 = False
                    tela_3 = True
                if event.key == pygame.K_SPACE:
                    tela_4 = False
                    tela_6 = True

    while tela_5:
        tela.fill(preto)
        mostra_uso_disco(270, 240)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_5 = False
                    tela_7 = True
                if event.key == pygame.K_LEFT:
                    tela_5 = False
                    tela_4 = True
                if event.key == pygame.K_SPACE:
                    tela_5 = False
                    tela_6 = True

    while tela_6:
        tela.fill(preto)
        mostra_uso_memoria(200, 180)
        mostra_uso_cpu(sur_cpu, psutil.cpu_percent(percpu=True), 8, 170, verde, cinza_escuro, branco)
        mostra_info_cpu(sur_infocpu, 8)
        mostra_uso_disco(360, 340)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    tela_6 = False
                    tela_1 = True

    while tela_7:
        tela.fill(preto)
        arquivos(20,50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_7 = False
                    tela_8 = True
                if event.key == pygame.K_LEFT:
                    tela_7 = False
                    tela_5 = True
                if event.key == pygame.K_SPACE:
                    tela_7 = False
                    tela_6 = True
    
    while tela_8:
        tela.fill(preto)
        maquinas_subrede(20,50, maquinas)
        postas_subrede(20, 70, maquinas)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    tela_8 = False
                    tela_1 = True
                if event.key == pygame.K_LEFT:
                    tela_8 = False
                    tela_7 = True
                if event.key == pygame.K_SPACE:
                    tela_8 = False
                    tela_6 = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        slide()

    pygame.display.update()