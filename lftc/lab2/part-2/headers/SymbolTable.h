#ifndef SYMBOLTABLE_H
#define SYMBOLTABLE_H

#include <string>
#include <vector>
using namespace std;

struct SymbolNode {
    string symbol;
    int index;
    SymbolNode* left;
    SymbolNode* right;
    
    SymbolNode(const string& sym, int idx);
};

class SymbolTable {
private:
    SymbolNode* root;
    int nextIndex;
    vector<string> indexToSymbol; // Pentru acces direct theta(1)
    
    SymbolNode* insert(SymbolNode* node, const string& symbol, int& index);
    SymbolNode* search(SymbolNode* node, const string& symbol);
    void inorderTraversal(SymbolNode* node, vector<pair<string, int>>& symbols);
    
public:
    SymbolTable();
    int addSymbol(const string& symbol);
    int findSymbol(const string& symbol);
    vector<pair<string, int>> getAllSymbols();
    string getSymbolByIndex(int index);
};

#endif