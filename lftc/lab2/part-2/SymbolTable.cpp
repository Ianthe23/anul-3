#include "headers/SymbolTable.h"

SymbolNode::SymbolNode(const string& sym, int idx) : symbol(sym), index(idx), left(nullptr), right(nullptr) {}

SymbolTable::SymbolTable() : root(nullptr), nextIndex(0) {}

SymbolNode* SymbolTable::insert(SymbolNode* node, const string& symbol, int& index) {
    if (!node) {
        index = nextIndex++;
        indexToSymbol.push_back(symbol); // Adaugă în vector pentru acces theta(1)
        return new SymbolNode(symbol, index);
    }
    
    if (symbol < node->symbol) {
        node->left = insert(node->left, symbol, index);
    } else if (symbol > node->symbol) {
        node->right = insert(node->right, symbol, index);
    } else {
        // Simbolul deja exista
        index = node->index;
    }
    
    return node;
}

SymbolNode* SymbolTable::search(SymbolNode* node, const string& symbol) {
    if (!node || node->symbol == symbol) {
        return node;
    }
    
    if (symbol < node->symbol) {
        return search(node->left, symbol);
    }
    
    return search(node->right, symbol);
}

void SymbolTable::inorderTraversal(SymbolNode* node, vector<pair<string, int>>& symbols) {
    if (node) {
        inorderTraversal(node->left, symbols);
        symbols.push_back({node->symbol, node->index});
        inorderTraversal(node->right, symbols);
    }
}

int SymbolTable::addSymbol(const string& symbol) {
    // Restrictie: identificatori de maxim 8 caractere
    // if (symbol.length() > 8) {
    //     return -1; // Eroare: identificator prea lung
    // }
    
    int index;
    root = insert(root, symbol, index);
    return index;
}

int SymbolTable::findSymbol(const string& symbol) {
    SymbolNode* node = search(root, symbol);
    return node ? node->index : -1;
}

vector<pair<string, int>> SymbolTable::getAllSymbols() {
    vector<pair<string, int>> symbols;
    inorderTraversal(root, symbols);
    return symbols;
}

// Acces direct theta(1) pe baza indexului din FIP
string SymbolTable::getSymbolByIndex(int index) {
    if (index >= 0 && index < indexToSymbol.size()) {
        return indexToSymbol[index];
    }
    return "";
}