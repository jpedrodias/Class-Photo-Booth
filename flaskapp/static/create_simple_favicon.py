"""
Favicon ICO simples criado manualmente
Representa uma câmera em 16x16 pixels
"""

import base64
import os

# Favicon ICO em base64 (16x16 pixels, câmera simples)
# Criado como um padrão de pixels que representa uma câmera
favicon_base64 = """
AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wDk5+3/2d3p/9nd6f/Z3en/2d3p/+Tn7f////8A////AP///wD///8A////AP///wD///8A////ANnd6f+AgID/AAAA/wAAAP8AAAD/AAAA/wAAAP+AgID/2d3p/////wD///8A////AP///wD///8A2d3p/wAAAP/f39//39/f/9/f3//f39//39/f/9/f3/8AAAD/2d3p/////wD///8A////AP///wDZ3en/AAAA/9/f3//39/f/9/f3//f39//39/f/9/f3/9/f3/8AAAD/2d3p/////wD///8A////ANnd6f8AAAD/39/f//f39/8ODg7/AAAA/wAAAP8ODg7/9/f3/9/f3/8AAAD/2d3p/////wD///8A////ANnd6f8AAAD/39/f//f39/8AAAD/AAAA/wAAAP8AAAD/9/f3/9/f3/8AAAD/2d3p/////wD///8A////ANnd6f8AAAD/39/f//f39/8ODg7/AAAA/wAAAP8ODg7/9/f3/9/f3/8AAAD/2d3p/////wD///8A////ANnd6f8AAAD/39/f//f39//39/f/9/f3//f39//39/f/9/f3/9/f3/8AAAD/2d3p/////wD///8A////ANnd6f8AAAD/39/f/9/f3//f39//39/f/9/f3//f39//39/f/9/f3/8AAAD/2d3p/////wD///8A////ANnd6f8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/2d3p/////wD///8A////AP///wDZ3en/gICA/4CAgP+AgID/gICA/4CAgP+AgID/gICA/4CAgP/Z3en/////AP///wD///8A////AP///wD///8A5Oft/9nd6f/Z3en/2d3p/9nd6f/Z3en/2d3p/+Tn7f////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==
"""

def create_favicon_ico():
    """Cria o arquivo favicon.ico a partir do base64"""
    try:
        # Decodificar base64
        favicon_data = base64.b64decode(favicon_base64.strip())
        
        # Salvar como favicon.ico
        with open('favicon.ico', 'wb') as f:
            f.write(favicon_data)
        
        print("✅ Favicon ICO criado com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar favicon: {e}")
        return False

if __name__ == "__main__":
    create_favicon_ico()
