
def check_parada(cur,parada):
    cur.execute(f"SELECT balance_banco FROM tabla_index WHERE nombre = '{parada}' ")
    check=cur.fetchall()
    for valor in check:
        if valor[0] > 1000.00:
            return True
        else: 
            return False
    
def listado_paradas(cur):
    cur.execute("SELECT nombre FROM tabla_index")  
    db_paradas=cur.fetchall()     
    return db_paradas

def info_parada(cur,parada):
    cur.execute(f"SELECT codigo,nombre,direccion,municipio,provincia,zona,cuota,pago FROM  tabla_index  WHERE nombre='{parada}'" )
    infos=cur.fetchall()     
    return infos

def info_cabecera(cur,parada):
    cur.execute(f"SELECT cuota, pago FROM tabla_index WHERE nombre = '{parada}'")
    resp=cur.fetchall()
    for repueta in resp:
      cuota=repueta[0]  
      pago=repueta[1]
          
    cur.execute(f'SELECT nombre FROM {parada}')
    seleccion=cur.fetchall()
    cant=len(seleccion)
       
    presidente = []       
    cur.execute(f"SELECT nombre FROM {parada}  WHERE funcion = 'Presidente'")   
    press=cur.fetchone()
    for pres in press:   
        presidente=pres 

    veedor = []
    cur.execute(f"SELECT nombre FROM {parada}  WHERE funcion = 'Veedor'")   
    presd=cur.fetchone()
    for prex in presd:
       veedor=prex    
    return cuota,pago,cant,presidente,veedor               
     
def lista_miembros(cur,parada):
    listas=[]
    cur.execute(f"SELECT codigo,nombre,cedula,telefono,funcion  FROM {parada}")
    miembros=cur.fetchall()
    for miembro in miembros:     
        listas+=miembro    
    lista=dividir_lista(listas,5)    
    return lista
    
def diario_general(cur,parada):
    prestamos=[]
    ingresos=[]
    gastos=[]
    aporte=[]
    pendiente=[]
    abonos=[]
    balance_bancario=[]
    cur.execute(f"SELECT  prestamos, ingresos, gastos, aporte, pendiente, abonos, balance_banco FROM tabla_index WHERE nombre='{parada}' " )  
    consult=cur.fetchall()
    for valor in consult:
      prestamos=valor[0]
      ingresos=valor[1]
      gastos=valor[2]
      aporte=valor[3]
      pendiente=valor[4]
      abonos=valor[5]
      balance_bancario=valor[6]
    balance=(aporte + ingresos + abonos )-(gastos+prestamos)
    data=(balance,prestamos,ingresos,gastos,aporte,pendiente,abonos,balance_bancario)   
    return data

def dividir_lista(lista,lon) : 
    return [lista[n:n+lon] for n in range(0,len(lista),lon)]     


def aportacion(cur,parada):           
    cur.execute(f"SELECT codigo, nombre, cedula, telefono, funcion FROM {parada}")
    data=cur.fetchall()
    return data
  
def verif_p(cur,parada,cedula,password):
    cur.execute(f"SELECT * FROM tabla_index WHERE  adm_password = '{password}'")
    result=cur.fetchall()
    if result:
      cur.execute(f"SELECT * FROM {parada} WHERE  cedula = '{cedula}'")                                       
      accounts =cur.fetchall()
      return accounts
    else: 
        return

def crear_p(cur,parada,string,valor_cuota,hoy):
       suma_no=[];suma_si=[]
       cur.execute(f'CREATE TABLE IF NOT EXISTS {parada}_cuota( item VARCHAR(50)  NULL, fecha VARCHAR(50)  NULL, estado VARCHAR(50)  NULL, nombre VARCHAR(50)  NULL, cedula VARCHAR(50)  NULL)')
       for data in string:
          cur.execute(f"INSERT INTO {parada}_cuota(item, fecha, estado, nombre, cedula) VALUES('{data[0]}', '{hoy}',  '{data[1]}', '{data[2]}', '{data[3]}')")    
       cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' ")   
       suma=cur.fetchall()
       for num in suma:
           suma_no=num[0]       
       cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' ")   
       sumas=cur.fetchall() 
       for numb in sumas:
           suma_si=numb[0]        
       n_aporte=int(suma_si) * float(valor_cuota)
       n_pendiente=int(suma_no) * float(valor_cuota)
       cur.execute(f"UPDATE tabla_index SET aporte={n_aporte}, pendiente={n_pendiente} WHERE nombre='{parada}'")
       return
   
def prestamo_aport(cur,parada):
    vgral=[]
    cur.execute(f"SELECT nombre FROM {parada}")
    list_nomb=cur.fetchall()
    for nombre in list_nomb:
        cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'pago' and nombre='{nombre[0]}'") 
        var_x = cur.fetchall()
        for var_p in var_x:
              var1=var_p[0]
        cur.execute(f"SELECT COUNT(estado) FROM {parada}_cuota WHERE estado = 'no_pago' and nombre='{nombre[0]}'")
        var_z = cur.fetchall()
        for var_n in var_z:
              var2=var_n[0]   
        sub_t=var1+var2      
        avg=round((var1/sub_t)*100,2)           
        vgral+=(nombre[0],var1,var2,sub_t,avg) 
    list_1=dividir_lista(vgral,5)                    
    return list_1

def verif_dig(cur,nombre,password):
    print(nombre,password)
    cur.execute(f"SELECT username FROM digitadores WHERE password='{password}'")
    result=cur.fetchall()
    if result !=[]:
       for valor in result:   
            if valor[0]==nombre:
               return True
            else:
              False
    else:
        return False
