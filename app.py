-- =======================================================
-- SCRIPT AUTO-FARM + HUB VISUAL: ROUBE UM OVO (ROBLOX)
-- Arquivo: script_roube_um_ovo.lua
-- =======================================================

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Workspace = game:GetService("Workspace")
local VirtualUser = game:GetService("VirtualUser")
local UserInputService = game:GetService("UserInputService")

local LocalPlayer = Players.LocalPlayer
local PlayerGui = LocalPlayer:WaitForChild("PlayerGui")
local Character = LocalPlayer.Character or LocalPlayer.CharacterAdded:Wait()

LocalPlayer.CharacterAdded:Connect(function(novoChar)
    Character = novoChar
end)

-- Configurações Globais (sincronizadas com o Streamlit)
if _G.AutoFarmOvos == nil then _G.AutoFarmOvos = true end
if _G.AutoMissoes == nil then _G.AutoMissoes = true end
if _G.AutoChocarOvos == nil then _G.AutoChocarOvos = false end
if _G.AutoRebirth == nil then _G.AutoRebirth = false end
_G.DistanciaColeta = _G.DistanciaColeta or 100
_G.NomeOvoParaChocar = _G.NomeOvoParaChocar or "Ovo Comum"

-- -------------------------------------------------------
-- 1. Interface Visual (GUI Flutuante Mobile & PC)
-- -------------------------------------------------------
if PlayerGui:FindFirstChild("RoubeUmOvoHub") then
    PlayerGui.RoubeUmOvoHub:Destroy()
end

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "RoubeUmOvoHub"
ScreenGui.ResetOnSpawn = false
ScreenGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
ScreenGui.Parent = PlayerGui

-- Botão flutuante para abrir/fechar o painel
local ToggleMenuBtn = Instance.new("TextButton")
ToggleMenuBtn.Name = "ToggleMenuBtn"
ToggleMenuBtn.Size = UDim2.new(0, 48, 0, 48)
ToggleMenuBtn.Position = UDim2.new(0, 15, 0.5, -24)
ToggleMenuBtn.BackgroundColor3 = Color3.fromRGB(25, 25, 35)
ToggleMenuBtn.Text = "🥚"
ToggleMenuBtn.TextSize = 24
ToggleMenuBtn.Font = Enum.Font.GothamBold
ToggleMenuBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
ToggleMenuBtn.Parent = ScreenGui

local ToggleCorner = Instance.new("UICorner")
ToggleCorner.CornerRadius = UDim.new(1, 0)
ToggleCorner.Parent = ToggleMenuBtn

local ToggleStroke = Instance.new("UIStroke")
ToggleStroke.Color = Color3.fromRGB(0, 200, 120)
ToggleStroke.Thickness = 2
ToggleStroke.Parent = ToggleMenuBtn

-- Janela Principal
local MainFrame = Instance.new("Frame")
MainFrame.Name = "MainFrame"
MainFrame.Size = UDim2.new(0, 255, 0, 320)
MainFrame.Position = UDim2.new(0.5, -127, 0.5, -160)
MainFrame.BackgroundColor3 = Color3.fromRGB(20, 22, 30)
MainFrame.BorderSizePixel = 0
MainFrame.Parent = ScreenGui

local MainCorner = Instance.new("UICorner")
MainCorner.CornerRadius = UDim.new(0, 12)
MainCorner.Parent = MainFrame

local MainStroke = Instance.new("UIStroke")
MainStroke.Color = Color3.fromRGB(55, 60, 80)
MainStroke.Thickness = 1.5
MainStroke.Parent = MainFrame

-- Barra de Título (Arrastável)
local TitleBar = Instance.new("Frame")
TitleBar.Name = "TitleBar"
TitleBar.Size = UDim2.new(1, 0, 0, 36)
TitleBar.BackgroundColor3 = Color3.fromRGB(30, 33, 45)
TitleBar.BorderSizePixel = 0
TitleBar.Parent = MainFrame

local TitleCorner = Instance.new("UICorner")
TitleCorner.CornerRadius = UDim.new(0, 12)
TitleCorner.Parent = TitleBar

local TitleText = Instance.new("TextLabel")
TitleText.Size = UDim2.new(1, -40, 1, 0)
TitleText.Position = UDim2.new(0, 12, 0, 0)
TitleText.BackgroundTransparency = 1
TitleText.Text = "🥚 Roube um Ovo Hub"
TitleText.TextColor3 = Color3.fromRGB(255, 255, 255)
TitleText.TextSize = 14
TitleText.Font = Enum.Font.GothamBold
TitleText.TextXAlignment = Enum.TextXAlignment.Left
TitleText.Parent = TitleBar

local CloseBtn = Instance.new("TextButton")
CloseBtn.Size = UDim2.new(0, 28, 0, 28)
CloseBtn.Position = UDim2.new(1, -32, 0, 4)
CloseBtn.BackgroundColor3 = Color3.fromRGB(200, 60, 60)
CloseBtn.Text = "—"
CloseBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
CloseBtn.TextSize = 14
CloseBtn.Font = Enum.Font.GothamBold
CloseBtn.Parent = TitleBar

local CloseCorner = Instance.new("UICorner")
CloseCorner.CornerRadius = UDim.new(0, 6)
CloseCorner.Parent = CloseBtn

-- Container dos Botões
local Container = Instance.new("Frame")
Container.Size = UDim2.new(1, -20, 1, -46)
Container.Position = UDim2.new(0, 10, 0, 42)
Container.BackgroundTransparency = 1
Container.Parent = MainFrame

local UIListLayout = Instance.new("UIListLayout")
UIListLayout.Padding = UDim.new(0, 7)
UIListLayout.SortOrder = Enum.SortOrder.LayoutOrder
UIListLayout.Parent = Container

local function criarBotaoToggle(texto, chaveGlobal, ordem)
    local btn = Instance.new("TextButton")
    btn.LayoutOrder = ordem
    btn.Size = UDim2.new(1, 0, 0, 36)
    btn.Font = Enum.Font.GothamSemibold
    btn.TextSize = 13
    btn.TextColor3 = Color3.fromRGB(255, 255, 255)
    btn.Parent = Container

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 8)
    corner.Parent = btn

    local function atualizarVisual()
        local ativo = _G[chaveGlobal]
        btn.Text = texto .. ": " .. (ativo and "ON" or "OFF")
        btn.BackgroundColor3 = ativo and Color3.fromRGB(35, 165, 95) or Color3.fromRGB(50, 54, 70)
    end

    btn.MouseButton1Click:Connect(function()
        _G[chaveGlobal] = not _G[chaveGlobal]
        atualizarVisual()
    end)

    atualizarVisual()
    return btn
end

criarBotaoToggle("Auto Farm Ovos", "AutoFarmOvos", 1)
criarBotaoToggle("Auto Missões", "AutoMissoes", 2)
criarBotaoToggle("Auto Chocar Ovos", "AutoChocarOvos", 3)
criarBotaoToggle("Auto Rebirth", "AutoRebirth", 4)

-- Seletor de Tipo de Ovo
local tiposOvos = {"Ovo Comum", "Ovo Raro", "Ovo Épico", "Ovo Lendário"}
local indiceOvo = 1
for i, nome in ipairs(tiposOvos) do
    if nome == _G.NomeOvoParaChocar then indiceOvo = i end
end

local OvoBtn = Instance.new("TextButton")
OvoBtn.LayoutOrder = 5
OvoBtn.Size = UDim2.new(1, 0, 0, 36)
OvoBtn.BackgroundColor3 = Color3.fromRGB(45, 90, 170)
OvoBtn.Font = Enum.Font.GothamSemibold
OvoBtn.TextSize = 13
OvoBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
OvoBtn.Text = "Ovo: " .. _G.NomeOvoParaChocar
OvoBtn.Parent = Container

local OvoCorner = Instance.new("UICorner")
OvoCorner.CornerRadius = UDim.new(0, 8)
OvoCorner.Parent = OvoBtn

OvoBtn.MouseButton1Click:Connect(function()
    indiceOvo = (indiceOvo % #tiposOvos) + 1
    _G.NomeOvoParaChocar = tiposOvos[indiceOvo]
    OvoBtn.Text = "Ovo: " .. _G.NomeOvoParaChocar
end)

-- Seletor de Distância
local distancias = {50, 100, 200, 300}
local indiceDist = 2
local DistBtn = Instance.new("TextButton")
DistBtn.LayoutOrder = 6
DistBtn.Size = UDim2.new(1, 0, 0, 36)
DistBtn.BackgroundColor3 = Color3.fromRGB(60, 65, 85)
DistBtn.Font = Enum.Font.GothamSemibold
DistBtn.TextSize = 13
DistBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
DistBtn.Text = "Distância Coleta: " .. tostring(_G.DistanciaColeta) .. " studs"
DistBtn.Parent = Container

local DistCorner = Instance.new("UICorner")
DistCorner.CornerRadius = UDim.new(0, 8)
DistCorner.Parent = DistBtn

DistBtn.MouseButton1Click:Connect(function()
    indiceDist = (indiceDist % #distancias) + 1
    _G.DistanciaColeta = distancias[indiceDist]
    DistBtn.Text = "Distância Coleta: " .. tostring(_G.DistanciaColeta) .. " studs"
end)

CloseBtn.MouseButton1Click:Connect(function()
    MainFrame.Visible = false
end)

ToggleMenuBtn.MouseButton1Click:Connect(function()
    MainFrame.Visible = not MainFrame.Visible
end)

-- Sistema de Arrastar (Touch e Mouse)
local dragging, dragInput, dragStart, startPos
TitleBar.InputBegan:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
        dragging = true
        dragStart = input.Position
        startPos = MainFrame.Position
        input.Changed:Connect(function()
            if input.UserInputState == Enum.UserInputState.End then
                dragging = false
            end
        end)
    end
end)

TitleBar.InputChanged:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch then
        dragInput = input
    end
end)

UserInputService.InputChanged:Connect(function(input)
    if input == dragInput and dragging then
        local delta = input.Position - dragStart
        MainFrame.Position = UDim2.new(startPos.X.Scale, startPos.X.Offset + delta.X, startPos.Y.Scale, startPos.Y.Offset + delta.Y)
    end
end)

-- -------------------------------------------------------
-- 2. Anti-AFK (Impede desconexão após 20 min)
-- -------------------------------------------------------
LocalPlayer.Idled:Connect(function()
    VirtualUser:Button2Down(Vector2.new(0, 0), Workspace.CurrentCamera.CFrame)
    task.wait(1)
    VirtualUser:Button2Up(Vector2.new(0, 0), Workspace.CurrentCamera.CFrame)
end)

-- -------------------------------------------------------
-- 3. Auto Farm (Coletar Ovos e Moedas com suporte a Model/Part)
-- -------------------------------------------------------
local function obterAlvoCFrame(instancia)
    if not instancia then return nil end
    if instancia:IsA("Attachment") then
        instancia = instancia.Parent
    end
    if instancia:IsA("BasePart") then
        return instancia.CFrame
    elseif instancia:IsA("Model") then
        return instancia:GetPivot()
    end
    return nil
end

local function coletarOvosProximos()
    while task.wait(0.15) do
        if _G.AutoFarmOvos then
            local rootPart = Character and Character:FindFirstChild("HumanoidRootPart")
            if rootPart then
                for _, object in pairs(Workspace:GetDescendants()) do
                    if not _G.AutoFarmOvos then break end

                    if object:IsA("ProximityPrompt") then
                        local alvo = object.Parent
                        if alvo and alvo:IsA("Attachment") then alvo = alvo.Parent end
                        if alvo and (alvo.Name:lower():find("ovo") or alvo.Name:lower():find("egg") or alvo.Name:lower():find("coin") or alvo.Name:lower():find("moeda")) then
                            local cf = obterAlvoCFrame(alvo)
                            if cf and (rootPart.Position - cf.Position).Magnitude <= _G.DistanciaColeta then
                                rootPart.CFrame = cf + Vector3.new(0, 3, 0)
                                pcall(function() fireproximityprompt(object) end)
                                task.wait(0.05)
                            end
                        end
                    elseif object:IsA("TouchTransmitter") and object.Parent then
                        local item = object.Parent
                        if item:IsA("BasePart") and (item.Name:lower():find("ovo") or item.Name:lower():find("egg") or item.Name:lower():find("coin") or item.Name:lower():find("moeda")) then
                            pcall(function()
                                firetouchinterest(rootPart, item, 0)
                                firetouchinterest(rootPart, item, 1)
                            end)
                        end
                    end
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- 4. Auto Missões
-- -------------------------------------------------------
local function gerenciarMissoes()
    while task.wait(2) do
        if _G.AutoMissoes then
            for _, v in pairs(ReplicatedStorage:GetDescendants()) do
                if v:IsA("RemoteEvent") and (v.Name:lower():find("quest") or v.Name:lower():find("missao") or v.Name:lower():find("claim")) then
                    pcall(function()
                        v:FireServer("All")
                        v:FireServer(1)
                        v:FireServer(true)
                    end)
                end
            end

            local missoesFolder = Workspace:FindFirstChild("Quests") or Workspace:FindFirstChild("Missoes") or Workspace:FindFirstChild("NPCs")
            if missoesFolder then
                for _, npc in pairs(missoesFolder:GetChildren()) do
                    local prompt = npc:FindFirstChildWhichIsA("ProximityPrompt", true)
                    if prompt then
                        pcall(function() fireproximityprompt(prompt) end)
                    end
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- 5. Auto Chocar Ovos (Hatch)
-- -------------------------------------------------------
local function chocarOvosAutomatico()
    while task.wait(0.5) do
        if _G.AutoChocarOvos then
            for _, v in pairs(ReplicatedStorage:GetDescendants()) do
                if v.Name:lower():find("hatch") or v.Name:lower():find("open") or v.Name:lower():find("egg") then
                    pcall(function()
                        if v:IsA("RemoteFunction") then
                            v:InvokeServer(_G.NomeOvoParaChocar, 1)
                        elseif v:IsA("RemoteEvent") then
                            v:FireServer(_G.NomeOvoParaChocar, 1)
                        end
                    end)
                end
            end
        end
    end
end

-- -------------------------------------------------------
-- 6. Auto Rebirth
-- -------------------------------------------------------
local function autoRebirth()
    while task.wait(3) do
        if _G.AutoRebirth then
            for _, v in pairs(ReplicatedStorage:GetDescendants()) do
                if v.Name:lower():find("rebirth") or v.Name:lower():find("renascer") then
                    pcall(function()
                        if v:IsA("RemoteEvent") then
                            v:FireServer()
                        elseif v:IsA("RemoteFunction") then
                            v:InvokeServer()
                        end
                    end)
                end
            end
        end
    end
end

task.spawn(coletarOvosProximos)
task.spawn(gerenciarMissoes)
task.spawn(chocarOvosAutomatico)
task.spawn(autoRebirth)

print("[ROUBE UM OVO] Hub visual carregado com sucesso!")
