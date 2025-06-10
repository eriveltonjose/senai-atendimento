import psycopg2

def conectar():
    return psycopg2.connect(
        dbname="assistencia",
        user="postgres",
        password="sua_senha",
        host="localhost"
    )

def registrar_cliente(conn, nome, email, telefone):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (%s, %s, %s)",
            (nome, email, telefone)
        )
        conn.commit()
        print("✅ Cliente cadastrado com sucesso.")

def listar_clientes(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT id, nome, email, telefone FROM clientes")
        clientes = cur.fetchall()
        print("\n📋 Lista de Clientes:")
        for cliente in clientes:
            print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Telefone: {cliente[3]}")

def registrar_chamado(conn, cliente_id, descricao):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO chamados (cliente_id, descricao, status) VALUES (%s, %s, %s)",
            (cliente_id, descricao, 'aberto')
        )
        conn.commit()
        print("📞 Chamado registrado com status 'aberto'.")

def listar_chamados_por_cliente(conn, cliente_id):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, descricao, status, data_abertura FROM chamados WHERE cliente_id = %s",
            (cliente_id,)
        )
        chamados = cur.fetchall()
        print(f"\n🛠️ Chamados do Cliente ID {cliente_id}:")
        for chamado in chamados:
            print(f"ID: {chamado[0]} | Desc: {chamado[1]} | Status: {chamado[2]} | Abertura: {chamado[3]}")

def atualizar_status_chamado(conn, chamado_id, novo_status):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE chamados SET status = %s WHERE id = %s",
            (novo_status, chamado_id)
        )
        conn.commit()
        print(f"📌 Chamado {chamado_id} atualizado para '{novo_status}'.")

def menu():
    print("\n=== Sistema de Atendimento Técnico ===")
    print("1. Cadastrar Cliente")
    print("2. Listar Clientes")
    print("3. Registrar Chamado")
    print("4. Listar Chamados por Cliente")
    print("5. Atualizar Status do Chamado")
    print("0. Sair")

if __name__ == "__main__":
    conn = conectar()
    try:
        while True:
            menu()
            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                nome = input("Nome: ")
                email = input("Email: ")
                telefone = input("Telefone: ")
                registrar_cliente(conn, nome, email, telefone)
            elif opcao == "2":
                listar_clientes(conn)
            elif opcao == "3":
                cliente_id = int(input("ID do Cliente: "))
                descricao = input("Descrição do Chamado: ")
                registrar_chamado(conn, cliente_id, descricao)
            elif opcao == "4":
                cliente_id = int(input("ID do Cliente: "))
                listar_chamados_por_cliente(conn, cliente_id)
            elif opcao == "5":
                chamado_id = int(input("ID do Chamado: "))
                novo_status = input("Novo status (aberto/em andamento/finalizado): ")
                atualizar_status_chamado(conn, chamado_id, novo_status)
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida.")
    except Exception as e:
        print("Erro:", e)
    finally:
        conn.close()
        print("🔒 Conexão encerrada.")
