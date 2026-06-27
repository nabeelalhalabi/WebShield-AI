export interface ExtractedTextItem {
  item_id: string;
  text: string;
  tag_name: string;
  page_url?: string;
  meta?: Record<string, unknown>;
}

export interface ExtractedImageItem {
  item_id: string;
  src: string;
  alt_text?: string;
  width: number;
  height: number;
  tag_name: string;
  page_url?: string;
  meta?: Record<string, unknown>;
}

export interface ExtractedPromoItem {
  item_id: string;
  text: string;
  tag_name: string;
  role?: string;
  class_name?: string;
  page_url?: string;
  meta?: Record<string, unknown>;
}

export interface ExtractedHeadingItem {
  item_id: string;
  text: string;
  level: number;
  page_url?: string;
  meta?: Record<string, unknown>;
}

export interface ExtractedPage {
  url: string;
  title: string;
  text_items: ExtractedTextItem[];
  image_items: ExtractedImageItem[];
  promo_items: ExtractedPromoItem[];
  headings: ExtractedHeadingItem[];
}
