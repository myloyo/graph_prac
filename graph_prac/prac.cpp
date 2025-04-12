#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <vector>
#include <list>
#include <map>
#include <locale>
#include <windows.h>
#include "Graph.h"

using namespace std;

int main() {
	setlocale(LC_ALL, "Russian");
	SetConsoleOutputCP(CP_UTF8);

	map<string, Graph> graphs;
	string cur = "";

	while (true) {
		cout << "\t~~Меню функций~~\n";
		cout << "1. Загрузить граф из файла\n";
		cout << "2. Выбрать текущий существующий граф\n";
		cout << "3. Создать свой граф\n";
		cout << "4. Показать список смежности текущего графа\n";
		cout << "5. Добавить вершину\n";
		cout << "6. Добавить ребро\n";
		cout << "7. Удалить вершину\n";
		cout << "8. Удалить ребро\n";
		cout << "9. Копировать граф\n";
		cout << "10. Задание 2 \n";
		cout << "11. Выйти\n";

		int x; cout << "Выберите действие: ";  
		cin >> x;
		if (x == 1) {
			Graph g;
			cout << "Введите название файла: ";
			string s; cin >> s;
			ifstream in(s);
			if (!in.is_open()) {
				throw runtime_error("Не удалось открыть файл для чтения.");
			}
			else{
				g.loadFromFile(s);
				graphs[s] = g;
				cur = s;
				cout << "\n";
			}
		}
		else if (x == 2) {
			cout << "Какой граф выбираем?\n";
			for (auto i : graphs) {
				cout << i.first << "\n";
			}
			string s;
			cin >> s;
			cur = s;
			cout << "Установлен текущий граф: " << s << "\n";
		}
		else if (x == 3) {

			Graph g1;
			string c1, c2;
			cout << "Граф взвешенный? ";
			cin >> c1;
			if (c1 == "yes" || c1 == "да") {
				g1.SetWeight(true);
			}
			else if (c1 == "no" || c1 == "нет") {
				g1.SetWeight(false);
			}

			cout << "Граф ориентированный? ";
			cin >> c2;
			if (c2 == "yes" || c2 == "да") {
				g1.SetDir(true);
			}
			else if (c2 == "no" || c2 == "нет") {
				g1.SetDir(false);
			}

			string u, v;
			int w;
			cout << "Вводите ребра графа, для завершения введите -1 -1 (и еще -1 если взвешенный)";
			if (g1.GetWeight()) {
				while (u != "-1" and v != "-1") {
					cin >> u >> v >> w;
					if (!g1.ExistVertex(u)) {
						g1.AddVertex(u);
					}
					if (!g1.ExistVertex(v)) {
						g1.AddVertex(v);
					}
					g1.AddEdge(u, v, w);
				}
			}
			else {
				while (u != "-1" and v != "-1") {
					cin >> u >> v;
					if (!g1.ExistVertex(u)) {
						g1.AddVertex(u);
					}
					if (!g1.ExistVertex(v)) {
						g1.AddVertex(v);
					}
					g1.AddEdge(u, v);
				}
			}

			string name;
			cout << "Введите название графа: ";
			cin >> name;
			cur = name;
			graphs[name] = g1;
		}
		else if (x == 4) {
			cout << cur << "\n";
			cout << "Список смежности для графа " << cur << "\n";
			graphs[cur].PrintList();
			cout << "\n";
		}
		else if (x == 5) {
			string u;
			cout << "Введите вершину: ";
			cin >> u;
			graphs[cur].AddVertex(u);
			cout << "\n";
		}
		else if (x == 6) {
			string u, v;
			cout << "Введите вершины: ";
			cin >> u >> v;
			if (graphs[cur].GetWeight() == true) {
				cout << "Введите вес ребра: ";
				int w; cin >> w;
				graphs[cur].AddEdge(u, v, w);
			}
			else {
				graphs[cur].AddEdge(u, v);
			}
			cout << "\n";
		}
		else if (x == 7) {
			string s;
			cout << "Введите вершину для удаления: ";
			cin >> s;
			graphs[cur].DeleteVertex(s);
			cout << "\n";
		}
		else if (x == 8) {
			string u, v;
			cout << "Введите ребро для удаления: ";
			cin >> u >> v;
			graphs[cur].DeleteEdge(u, v);
		}
		else if (x == 9) {
			string name;
			cout << "Введите имя графа, в который копируем текущий граф: ";
			cin >> name;
			graphs[name](graphs[cur]);
			cout << "Граф успешно скопирован!\n";
		}
		else if (x == 10) {
			graphs[cur].Task2();
		}
		else if (x == 11) {
			cout << "Работа с графами завершена.\n";
			exit(0);
		}
	}
}