/**
 * TrueNorth Sidebar Tree View Provider
 *
 * Provides a custom sidebar panel with agent launcher, project status,
 * and quick actions for a vibe coder-friendly experience.
 */
import * as vscode from 'vscode';
import { ModeManager } from '../modes';
export interface ISidebarItem {
    id: string;
    label: string;
    icon?: string;
    description?: string;
    command?: string;
    children?: ISidebarItem[];
    contextValue?: string;
    collapsibleState?: vscode.TreeItemCollapsibleState;
    tooltip?: string;
}
export declare class TrueNorthSidebarProvider implements vscode.TreeDataProvider<ISidebarItem> {
    private context;
    private _onDidChangeTreeData;
    readonly onDidChangeTreeData: vscode.Event<ISidebarItem | undefined | null | void>;
    private projectStatus;
    private modeManager?;
    constructor(context: vscode.ExtensionContext);
    setModeManager(modeManager: ModeManager): void;
    updateModeStatus(): void;
    refresh(): void;
    getTreeItem(element: ISidebarItem): vscode.TreeItem;
    getChildren(element?: ISidebarItem): Promise<ISidebarItem[]>;
    private getRootItems;
    private getHealthIcon;
    private getHealthDescription;
    private getProjectStatusChildren;
    private getQuickActionChildren;
    private getAnalysisAgentChildren;
    private getImprovementAgentChildren;
    private getDeploymentAgentChildren;
    private getRecentActivityChildren;
    updateProjectStatus(status: Partial<typeof this.projectStatus>): void;
    updateAgentCounts(running: number, completed: number, failed: number): void;
    setProjectHealth(health: 'good' | 'warning' | 'error'): void;
    private getModeChildren;
    private getModeActionChildren;
}
/**
 * Enhanced webview provider for the TrueNorth sidebar with comprehensive dashboard UI
 */
export declare class TrueNorthWebviewProvider implements vscode.WebviewViewProvider {
    private readonly _context;
    private modeManager?;
    static readonly viewType = "truenorth-sidebar";
    private _view?;
    private _statusData;
    constructor(_context: vscode.ExtensionContext);
    setModeManager(modeManager: ModeManager): void;
    resolveWebviewView(webviewView: vscode.WebviewView): void;
    private _getHtmlForWebview;
    updateCounts(running: number, completed: number, failed: number): void;
    updateStatus(status: string, type?: string): void;
    updatePhase(phase: string): void;
    updateProgress(progress: number): void;
    setProjectHealth(health: 'good' | 'warning' | 'error'): void;
    show(): void;
}
//# sourceMappingURL=TrueNorthSidebarProvider.d.ts.map