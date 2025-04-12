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
		cout << "\t~~���� �������~~\n";
		cout << "1. ��������� ���� �� �����\n";
		cout << "2. ������� ������� ������������ ����\n";
		cout << "3. ������� ���� ����\n";
		cout << "4. �������� ������ ��������� �������� �����\n";
		cout << "5. �������� �������\n";
		cout << "6. �������� �����\n";
		cout << "7. ������� �������\n";
		cout << "8. ������� �����\n";
		cout << "9. ���������� ����\n";
		cout << "10. ������� 2 \n";
		cout << "11. �����\n";

		int x; cout << "�������� ��������: ";  
		cin >> x;
		if (x == 1) {
			Graph g;
			cout << "������� �������� �����: ";
			string s; cin >> s;
			ifstream in(s);
			if (!in.is_open()) {
				throw runtime_error("�� ������� ������� ���� ��� ������.");
			}
			else{
				g.loadFromFile(s);
				graphs[s] = g;
				cur = s;
				cout << "\n";
			}
		}
		else if (x == 2) {
			cout << "����� ���� ��������?\n";
			for (auto i : graphs) {
				cout << i.first << "\n";
			}
			string s;
			cin >> s;
			cur = s;
			cout << "���������� ������� ����: " << s << "\n";
		}
		else if (x == 3) {

			Graph g1;
			string c1, c2;
			cout << "���� ����������? ";
			cin >> c1;
			if (c1 == "yes" || c1 == "��") {
				g1.SetWeight(true);
			}
			else if (c1 == "no" || c1 == "���") {
				g1.SetWeight(false);
			}

			cout << "���� ���������������? ";
			cin >> c2;
			if (c2 == "yes" || c2 == "��") {
				g1.SetDir(true);
			}
			else if (c2 == "no" || c2 == "���") {
				g1.SetDir(false);
			}

			string u, v;
			int w;
			cout << "������� ����� �����, ��� ���������� ������� -1 -1 (� ��� -1 ���� ����������)";
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
			cout << "������� �������� �����: ";
			cin >> name;
			cur = name;
			graphs[name] = g1;
		}
		else if (x == 4) {
			cout << cur << "\n";
			cout << "������ ��������� ��� ����� " << cur << "\n";
			graphs[cur].PrintList();
			cout << "\n";
		}
		else if (x == 5) {
			string u;
			cout << "������� �������: ";
			cin >> u;
			graphs[cur].AddVertex(u);
			cout << "\n";
		}
		else if (x == 6) {
			string u, v;
			cout << "������� �������: ";
			cin >> u >> v;
			if (graphs[cur].GetWeight() == true) {
				cout << "������� ��� �����: ";
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
			cout << "������� ������� ��� ��������: ";
			cin >> s;
			graphs[cur].DeleteVertex(s);
			cout << "\n";
		}
		else if (x == 8) {
			string u, v;
			cout << "������� ����� ��� ��������: ";
			cin >> u >> v;
			graphs[cur].DeleteEdge(u, v);
		}
		else if (x == 9) {
			string name;
			cout << "������� ��� �����, � ������� �������� ������� ����: ";
			cin >> name;
			graphs[name](graphs[cur]);
			cout << "���� ������� ����������!\n";
		}
		else if (x == 10) {
			graphs[cur].Task2();
		}
		else if (x == 11) {
			cout << "������ � ������� ���������.\n";
			exit(0);
		}
	}
}