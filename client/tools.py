def get_tools():
    return [
    {
        "function_declarations": [
            {
                "name": "tiempo_sistema",
                "description": "Devuelve la fecha y hora actual del sistema local.",
            },
            {
                "name": "obtener_metricas_sistema",
                "description": "Obtiene metricas del sistema.",
            },
            {
                "name": "listar_procesos_top",
                "description": "Obtiene los procesos que mas consumen memoria RAM del sistema.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "limite": {
                            "type": "INTEGER",
                            "description": "La cantidad de procesos a obtener (ej: 10)",
                            "default":10
                        },
                        "tipo": {
                            "type": "STRING",
                            "description": "El tipo de proceso a obtener (cpu, ram)",
                            "default": "cpu",
                            "enum": ["cpu", "ram"]
                        }
                    },
                    "required": ["limite", "tipo"]
                }
            },{
                "name": "listar_procesos_en_puertos",
                "description": "Lista los puertos con procesos en uso del sistema.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "protocol": {
                            "type": "STRING",
                            "description": "El protocolo a obtener (tcp, udp o ambos)",
                            "default": "all",
                            "enum": ["all", "tcp", "udp"]
                        }
                    },
                    "required": ["protocol"]
                }
            },{
                "name": "verificar_proceso_en_puerto",
                "description": "Verifica si un puerto está en uso y muestra el proceso que lo está utilizando.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "port": {
                            "type": "INTEGER",
                            "description": "El puerto a verificar (ej: 80)",
                        }
                    },
                    "required": ["port"]
                }
            },
            {
                "name": "matar_proceso_en_puerto",
                "description": " Mata el proceso que está utilizando un puerto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "port": {
                            "type": "INTEGER",
                            "description": "El puerto a matar (ej: 80)",
                        }
                    },
                    "required": ["port"]
                }
            }
        ]
    }
]