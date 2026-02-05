import asyncio
from google import genai
from google.genai import types

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from tools import get_tools 
from config import mcp_client, api_key, ia_model

# Configuración de Rich
console = Console()

gemini_client = genai.Client()



async def main():
    try:
        async with mcp_client:
            console.print(Panel.fit("[bold blue]Cliente MCP con Gemini[/bold blue]", title="Bienvenido"))
            
            #Creacion del chat con GEMINI
            #valid_models = [m.name for m in gemini_client.models.list()]
            #console.print(f"[dim]Modelos de IA disponibles:[/dim] {', '.join(valid_models)}\n")
            
            chat = gemini_client.aio.chats.create(
                model=ia_model,
                config=types.GenerateContentConfig(
                    tools=get_tools(),
                    system_instruction="""
ROL: Eres un Ingeniero Experto en DevOps y Administración de Sistemas (SysAdmin). Tu prioridad es la estabilidad del sistema.

PROTOCOLO DE SEGURIDAD PARA 'MATAR PROCESOS':

Fase 1: INVESTIGACIÓN (Automática)
Si el usuario pide liberar un puerto o matar un proceso:
1. NO ejecutes la acción de inmediato.
2. EJECUTA PRIMERO la herramienta `verificar_proceso_en_puerto` o `listar_procesos_en_puertos` para identificar con certeza qué corre ahí.
3. ANALIZA el resultado:
- Si el proceso es crítico para el sistema (ej: root, kernel, systemd, svchost, antivirus), INFORMA al usuario del alto riesgo y sugiere no hacerlo.

Fase 2: CONFIRMACIÓN (Interacción)
Presenta un informe claro al usuario con este formato:
"⚠️ **ALERTA DE SEGURIDAD**
El puerto [X] está siendo usado por:
- **Proceso:** [Nombre del Proceso]
- **PID:** [ID del proceso]
- **Impacto:** [Tu análisis breve sobre qué pasará si se cierra]

¿Estás absolutamente seguro de querer terminar este proceso? (Responde 'SÍ' para proceder)"

Fase 3: EJECUCIÓN
- SOLO si el usuario confirma explícitamente (Sí/Yes/Confirmar), ejecuta la herramienta `matar_proceso_en_puerto`.
- Si el usuario duda o dice "No", cancela la operación y confirma que no se hicieron cambios.

NOTA TÉCNICA: Si la herramienta devuelve error de permisos, sugiere al usuario ejecutar el cliente con privilegios de administrador/sudo.
"""
                ),
            )

            while True:
                prompt_text = Prompt.ask("\n[bold green]👤 Usuario[/bold green]")
                
                if prompt_text.lower() in ["exit", "salir", "quit"]:
                    console.print("[bold red]Saliendo...[/bold red]")
                    break

                with console.status("[bold blue]🤖 Gemini está pensando...", spinner="dots"):
                    response = await chat.send_message(prompt_text)
                    part = response.parts[0]

                    if fn:= part.function_call:
                        console.print(f"[dim]🤖 Gemini quiere usar la herramienta:[/dim] [bold cyan]{fn.name}[/bold cyan]")
                        console.print(f"[dim]Con argumentos:[/dim] {fn.args}")
                        
                        try:
                            result = await mcp_client.call_tool(fn.name, arguments=fn.args)
                            console.print(f"[dim]🤖 Resultado de la herramienta:[/dim]\n{result.content[0].text}\n")

                            #Respuesta final con el resultado de la herramienta
                            response_final = await chat.send_message(
                                types.Part(
                                    function_response=types.FunctionResponse(
                                        name=fn.name,
                                        response={'result': result.content[0].text},
                                    )
                                )
                            )
                            console.print(Panel(Markdown(response_final.text), title="🤖 Gemini", border_style="blue"))
                        except Exception as tool_error:
                            console.print(f"[bold red]Error ejecutando herramienta:[/bold red] {tool_error}")
                            # Send error back to Gemini so it knows what happened? Optional but good interaction.
                            # For now just print to user.
                    else:
                         console.print(Panel(Markdown(part.text), title="🤖 Gemini", border_style="blue"))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    asyncio.run(main())