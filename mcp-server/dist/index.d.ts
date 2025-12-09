#!/usr/bin/env node
/**
 * TopEndSports Content Briefs MCP Server
 *
 * Provides tools for the content briefs generation system:
 * - Site structure lookup (CSV search)
 * - Brand rules and positioning
 * - Brief management (list active/completed)
 * - Document conversion (markdown to docx)
 * - Feedback submission
 */
export declare const findProjectRoot: () => string;
export declare const BRAND_RULES: {
    locked_positions: {
        position_1: {
            brand: string;
            status: string;
            rationale: string;
        };
        position_2: {
            brand: string;
            status: string;
            rationale: string;
        };
    };
    tier_1_brands: string[];
    tier_2_brands: string[];
    tier_3_brands: string[];
    brand_guidelines: {
        FanDuel: {
            usp: string;
            key_features: string[];
            typical_position: number;
        };
        BetMGM: {
            usp: string;
            key_features: string[];
            typical_position: number;
        };
        DraftKings: {
            usp: string;
            key_features: string[];
            typical_position: number;
        };
        Caesars: {
            usp: string;
            key_features: string[];
            typical_position: number;
        };
        bet365: {
            usp: string;
            key_features: string[];
            typical_position: number;
        };
        Fanatics: {
            usp: string;
            key_features: string[];
            typical_position: number;
            badge_code: string;
            badge_color: string;
        };
        "theScore BET": {
            usp: string;
            key_features: string[];
            typical_position: number;
            badge_code: string;
            badge_color: string;
            notes: string;
        };
    };
    compliance_rules: {
        age_requirement_default: string;
        age_requirement_exceptions: string[];
        gambling_hotline: string;
        affiliate_disclosure_required: boolean;
        responsible_gambling_section_required: boolean;
        forbidden_language: string[];
    };
    writer_assignments: {
        "Lewis Humphries": {
            priority: string[];
            content_types: string[];
        };
        "Tom Goldsmith": {
            priority: string[];
            content_types: string[];
        };
        "Gustavo Cantella": {
            priority: string[];
            content_types: string[];
            special_rules: string[];
        };
    };
};
export declare let siteStructureEnglish: any[];
export declare let siteStructureSpanish: any[];
export declare const setSiteStructureData: (english: any[], spanish: any[]) => void;
export declare const loadCSVData: () => void;
export declare const searchSiteStructure: (query: string, language?: string) => any[];
export declare const getPageByUrl: (url: string) => any | null;
export declare const listBriefs: (directory: string) => any[];
//# sourceMappingURL=index.d.ts.map