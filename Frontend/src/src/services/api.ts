const API_BASE_URL = "http://localhost:8000";

export interface BackendProduct {
    _id: string;
    productName: string;
    productImage: string;
    productURL: string;
    originalPrice: number;
    discountedPrice: number;
    discount: number;
    availableAt: string;
}

export interface ApiResponse {
    success: boolean;
    status: number;
    count: number;
    data: BackendProduct[];
}

export const fetchAlFatahProducts = async (): Promise<ApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/alfatah`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
};

export const fetchMetroProducts = async (): Promise<ApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/metro`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
};

export const fetchJalalSonsProducts = async (): Promise<ApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/jalalsons`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
};

export const fetchRajaSahibProducts = async (): Promise<ApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/rajasahib`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
};

export const fetchRahimStoreProducts = async (): Promise<ApiResponse> => {
    const response = await fetch(`${API_BASE_URL}/rahimstore`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
};

export type StoreFetcher = () => Promise<ApiResponse>;

export const getStoreFetcher = (storeSlug: string): StoreFetcher | null => {
    const fetcherMap: Record<string, StoreFetcher> = {
        "al-fatah": fetchAlFatahProducts,
        "metro": fetchMetroProducts,
        "jalal-sons": fetchJalalSonsProducts,
        "raja-sahib": fetchRajaSahibProducts,
        "rahim-store": fetchRahimStoreProducts,
    };
    return fetcherMap[storeSlug] || null;
};
