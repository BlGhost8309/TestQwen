import subprocess
import platform
import re
import sys

def ping_host(host, duration=10):
    """
    Пингует хост в течение заданного времени.
    Возвращает кортеж: (успех, среднее_время, количество_ответов)
    """
    system = platform.system()
    try:
        if system == "Windows":
            # На Windows: -n количество пакетов, -w таймаут в мс
            # Пингуем 10 раз с таймаутом 1 секунду (имитация 10 секунд)
            cmd = ["ping", "-n", str(duration), "-w", "1000", host]
            # Кодировка cp866 для русской версии Windows
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=duration + 5)
            output_str = output.decode('cp866', errors='ignore')
            
            # Ищем время ответа в русском формате: "время=25мс" или "время<1мс"
            times = re.findall(r'время[=<](\d+)мс', output_str)
            # Дублирующая проверка для английского формата (на случай англ. винды)
            if not times:
                times = re.findall(r'time[=<](\d+)ms', output_str)
                
        else:
            # Linux/Mac: -c количество, -W таймаут в секундах
            cmd = ["ping", "-c", str(duration), "-W", "1", host]
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=duration + 5)
            output_str = output.decode('utf-8', errors='ignore')
            times = re.findall(r'time[=<](\d+\.?\d*)\s*ms', output_str)

        if times:
            float_times = [float(t) for t in times]
            avg_time = sum(float_times) / len(float_times)
            return True, avg_time, len(times)
        else:
            return False, 0, 0

    except subprocess.CalledProcessError:
        return False, 0, 0
    except Exception as e:
        print(f"Ошибка при пинге {host}: {e}")
        return False, 0, 0

def main():
    # 5 известных поисковых систем
    hosts = ["google.com", "bing.com", "yahoo.com", "duckduckgo.com", "yandex.com"]
    duration = 10
    
    print(f"Начинаем пинговать 5 поисковых систем в течение {duration} секунд каждая...")
    print("-" * 60)
    
    results = {}
    
    for host in hosts:
        print(f"\nПингуем {host}...")
        success, avg, count = ping_host(host, duration)
        
        if success and count > 0:
            print(f"  {host}: получено {count} ответов, среднее время: {avg:.2f} мс")
            results[host] = avg
        else:
            print(f"  {host}: нет данных о времени ответа (хост недоступен или блокирует ICMP)")
            results[host] = None

    print("\n" + "=" * 60)
    
    valid_results = [v for v in results.values() if v is not None]
    
    if valid_results:
        overall_avg = sum(valid_results) / len(valid_results)
        print(f"Общая средняя скорость по доступным хостам: {overall_avg:.2f} мс")
    else:
        print("Не удалось получить данные о скорости пинга ни от одного хоста.")
        print("Возможно, отсутствует интернет или блокируются ICMP-запросы фаерволом.")

if __name__ == "__main__":
    main()
