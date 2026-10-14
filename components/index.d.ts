import type * as React from 'react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** primary: matcha by day, peony by evening. quiet: outlined. ghost: underlined text. */
  variant?: 'primary' | 'quiet' | 'ghost';
  size?: 'md' | 'sm';
}
export declare function Button(props: ButtonProps): React.ReactElement;

export interface TagProps { tone?: 'neutral' | 'matcha' | 'peony' | 'wine' | 'candle'; children?: React.ReactNode }
export declare function Tag(props: TagProps): React.ReactElement;

export interface OpenNowProps {
  /** day = coffee and matcha; evening = wine and meze. */
  part: 'day' | 'evening';
  /** 24-hour clock, e.g. "17:00". Defaults: 17:00 by day, 00:00 by evening. */
  until?: string;
  /** What is being served, in Albanian. Defaults: "kafe e matcha" / "verë e meze". */
  serving?: string;
}
export declare function OpenNow(props: OpenNowProps): React.ReactElement;

export interface MenuItemProps {
  name: string;
  note?: string;
  /** Formatted price, euro sign first: "€3.50". */
  price: string;
  tag?: string;
  tagTone?: TagProps['tone'];
}
export declare function MenuItem(props: MenuItemProps): React.ReactElement;

export interface BouquetSize { id: string; price: string }
export interface BouquetCardProps {
  name: string;
  note?: string;
  tag?: string;
  /** Colour of the art panel. */
  tone?: 'peony' | 'matcha' | 'wine' | 'candle';
  sizes?: BouquetSize[];
  defaultSize?: string;
  onSizeChange?: (id: string) => void;
  onOrder?: () => void;
  /** Button label. Default "Porosit". */
  cta?: string;
}
export declare function BouquetCard(props: BouquetCardProps): React.ReactElement;

export interface FieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  hint?: string;
  error?: string;
  multiline?: boolean;
}
export declare function Field(props: FieldProps): React.ReactElement;

declare global {
  interface Window {
    Clover: { Button: typeof Button; Tag: typeof Tag; OpenNow: typeof OpenNow; MenuItem: typeof MenuItem; BouquetCard: typeof BouquetCard; Field: typeof Field };
  }
}
