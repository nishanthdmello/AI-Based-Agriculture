// app/api/calculate/route.js
import { NextResponse } from 'next/server';

export async function POST(req) {
  const { npk, soilMoisture, crop } = await req.json();

  // Dummy calculation for feasibility (replace with actual logic)
  const feasibility = Math.min(
    100,
    Math.max(
      0,
      (parseFloat(npk.n) + parseFloat(npk.p) + parseFloat(npk.k) + parseFloat(soilMoisture)) / 4
    )
  );

  return NextResponse.json({ feasibility });
}
