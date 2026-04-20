# Test file
import subprocess
import time
import statistics

# Список известных поисковых систем для пинга
search_engines = [
    "google.com",
    "bing.com",
    "yahoo.com",
    "duckduckgo.com",
    "yandex.com"
]

def ping_host(host, duration=10):
    """Пингует хост в течение указанного времени и возвращает список времен ответа."""
    times = []
    start_time = time.time()
    
    try:
        # Запускаем ping с интервалом 1 секунду
        process = subprocess.Popen(
            ["ping", "-c", "1000", "-i", "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        end_time = start_time + duration
        
        while time.time() < end_time:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            # Парсим время ответа из строки ping
            if "time=" in line:
                try:
                    # Извлекаем значение времени (например, time=12.3 ms)
                    time_part = line.split("time=")[1].split()[0]
                    ping_time = float(time_part.replace("ms", ""))
                    times.append(ping_time)
                except (ValueError, IndexError):
                    continue
        
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"Ошибка при пинге {host}: {e}")
    
    return times

def main():
    all_times = []
    
    print("Начинаем пинговать 5 поисковых систем в течение 10 секунд каждая...")
    print("-" * 60)
    
    for engine in search_engines:
        print(f"\nПингуем {engine}...")
        times = ping_host(engine, duration=10)
        
        if times:
            avg_time = statistics.mean(times)
            print(f"  {engine}: получено {len(times)} ответов, среднее время: {avg_time:.2f} ms")
            all_times.extend(times)
        else:
            print(f"  {engine}: нет данных о времени ответа")
    
    print("\n" + "=" * 60)
    
    if all_times:
        overall_avg = statistics.mean(all_times)
        print(f"Общая средняя скорость пинга по всем поисковым системам: {overall_avg:.2f} ms")
    else:
        print("Не удалось получить данные о скорости пинга")

if __name__ == "__main__":
    main()
