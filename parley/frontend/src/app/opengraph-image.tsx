import { ImageResponse } from "next/og";

export const alt = "Parley: soon your AI will negotiate with mine. See how they behave before it counts.";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: 80,
          background: "#ffffff",
          borderTop: "16px solid #1f2d5c",
          color: "#000000",
        }}
      >
        <div style={{ fontSize: 36, fontWeight: 600 }}>Parley</div>
        <div style={{ display: "flex", flexDirection: "column", fontSize: 72, fontWeight: 600, lineHeight: 1.05 }}>
          <span>Soon your AI will negotiate with mine.</span>
          <span style={{ color: "#1f2d5c" }}>See how they behave before it counts.</span>
        </div>
        <div style={{ fontSize: 28, color: "#1f2d5c" }}>Any scene · Any agent · Every move on the record</div>
      </div>
    ),
    size,
  );
}
